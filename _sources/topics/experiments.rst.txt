===========
Experiments
===========

Gluepy supports autonomous, long-running experimentation where an AI coding agent iteratively improves a DAG's work tasks while evaluation tasks remain frozen. This ensures all improvements are genuine and metrics cannot be gamed.

Overview
========

The experiment system adds three concepts to Gluepy:

1. **EvaluationTask** -- a ``Task`` subclass for evaluation steps that must remain untouched during experiments.
2. **eval_tasks** -- a new attribute on ``DAG`` that separates evaluation from work.
3. **Structured metrics output** -- a machine-readable block printed after evaluation, enabling agents to parse results.

An AI agent (Claude Code, Cursor, etc.) drives the experiment loop: it modifies work task code, runs the DAG, reads the metrics, and decides whether to keep or revert changes.


Adding eval_tasks to a DAG
==========================

Add an ``eval_tasks`` list to your DAG alongside the existing ``tasks``:

.. code-block:: python

    from gluepy.exec import DAG, EvaluationTask
    from gluepy.ops import default_mlops
    from .tasks import PrepareDataTask, TrainModelTask, PredictTask


    class ComputeAccuracyTask(EvaluationTask):
        """Computes forecast accuracy metrics.

        Metrics:
            forecast_mape (float): Mean Absolute Percentage Error.
                Primary measure of forecast accuracy. Lower is better.
            forecast_bias (float): Systematic directional error.
                Closer to 0.0 is better.
        """
        label = "compute_accuracy"

        def run(self):
            # ... compute metrics ...
            default_mlops.log_metric("forecast_mape", mape_score)
            default_mlops.log_metric("forecast_bias", mean_bias)


    class ForecastDAG(DAG):
        label = "forecast"
        tasks = [PrepareDataTask, TrainModelTask, PredictTask]
        eval_tasks = [ComputeAccuracyTask]

If ``eval_tasks`` is omitted, the DAG behaves exactly as before -- fully backward compatible.


Writing EvaluationTask Subclasses
=================================

``EvaluationTask`` is a subclass of ``Task``. The key contract is:

1. Call ``default_mlops.log_metric(key, value)`` for every metric computed.
2. Document metrics and their significance in the class docstring.
3. The agent reads docstrings to understand what "improvement" means -- no explicit ``primary_metric`` tagging needed.

Write descriptive docstrings that explain:

- What each metric measures
- What direction is "better" (lower/higher/closer to a target)
- How metrics relate to each other
- Any hard constraints (e.g., "must be 1.0")

.. code-block:: python

    class ValidateOutputTask(EvaluationTask):
        """Validates ETL output correctness.

        Metrics:
            row_count_match (float): 1.0 if output row count matches
                expected, 0.0 otherwise. Must be 1.0.
            processing_time_seconds (float): Wall-clock time for the
                pipeline. Lower is better.
        """
        label = "validate_output"

        def run(self):
            # ... validation logic ...
            default_mlops.log_metric("row_count_match", 1.0 if valid else 0.0)
            default_mlops.log_metric("processing_time_seconds", elapsed)


CLI Flags
=========

The ``dag`` command supports several flags for evaluation control:

.. code-block:: bash

    # Run work tasks + evaluation tasks (default)
    python manage.py dag forecast

    # Skip evaluation tasks
    python manage.py dag forecast --skip-eval

    # Run only evaluation tasks on an existing run
    python manage.py dag forecast --eval-only --retry <run_folder>

    # Compare metrics across runs
    python manage.py dag forecast --compare <run_folder_1> <run_folder_2>

``--eval-only`` requires ``--retry`` because evaluation tasks need an existing run's output to evaluate.

``--skip-eval`` and ``--eval-only`` are mutually exclusive.

``--compare`` reads ``metrics.json`` from each run folder and prints a TSV table for easy comparison.


Structured Metrics Output
=========================

After evaluation tasks run, the DAG runner prints a machine-readable block to stdout:

.. code-block:: text

    === GLUEPY METRICS ===
    metric:forecast_mape=12.5
    metric:forecast_bias=-0.03
    === END METRICS ===

This uses ``print()`` (not ``logger.info()``) so agents can reliably extract metrics with ``grep "^metric:"`` regardless of logging configuration.

Metrics are also persisted to ``metrics.json`` in the run folder for programmatic access and the ``--compare`` feature.


Running Experiments with Claude Code
=====================================

After installing the skill (``python manage.py skill claude``), use the ``/experiment`` command:

.. code-block:: text

    /experiment forecast "improve the MAPE score"

The agent will:

1. Verify git is available and the project is a git repository
2. Run a setup checklist with you (frozen paths, baseline metrics)
3. Create an experiment branch
4. Enter an autonomous loop: modify code, run DAG, evaluate, keep/revert

For Cursor users, run ``python manage.py skill cursor`` and use the same ``/experiment`` command.


Customizing Frozen Paths
=========================

During setup, the agent agrees with you on which paths are frozen (cannot be modified). The defaults are:

- Evaluation task modules (files containing ``EvaluationTask`` subclasses)
- ``setup.py``, ``pyproject.toml``
- ``Dockerfile*``, ``.dockerignore``
- ``.github/workflows/``

Everything else is fair game, including configs, dependencies, tests, and DAG definitions.


Interpreting experiment_log.tsv
===============================

The experiment log tracks all experiments as a TSV file:

.. list-table::
   :header-rows: 1

   * - Column
     - Description
   * - experiment_id
     - Sequential integer
   * - timestamp
     - ISO 8601 timestamp
   * - run_id
     - Gluepy run ID
   * - metrics
     - All metrics as semicolon-separated key=value pairs
   * - status
     - ``keep``, ``discard``, ``crash``, or ``timeout``
   * - description
     - What was changed
   * - commit
     - Git commit hash
   * - duration_seconds
     - Wall-clock time for the run


Tips for Writing DAGs That Experiment Well
==========================================

- **Clear metric docstrings**: The agent's decision quality depends on understanding what metrics mean.
- **Fast execution**: Shorter DAG runs mean more experiments per hour. Consider using data subsets during experimentation.
- **Deterministic evaluation**: Non-deterministic evaluations add noise. Average over multiple samples if needed.
- **Modular work tasks**: Smaller, focused tasks are easier for the agent to modify without breaking things.
- **Good defaults**: Start with reasonable hyperparameters so the agent has a solid baseline to improve from.
