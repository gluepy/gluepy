# Experiments

## EvaluationTask

`EvaluationTask` is a subclass of `Task` for evaluation steps that must remain frozen during experiments.

```python
from gluepy.exec import EvaluationTask
from gluepy.ops import default_mlops

class ComputeAccuracyTask(EvaluationTask):
    """Computes forecast accuracy metrics.

    Metrics:
        forecast_mape (float): Mean Absolute Percentage Error.
            Lower is better.
        forecast_bias (float): Systematic over/under-forecasting.
            Closer to 0.0 is better.
    """
    label = "compute_accuracy"

    def run(self):
        # ... compute metrics ...
        default_mlops.log_metric("forecast_mape", mape_score)
        default_mlops.log_metric("forecast_bias", mean_bias)
```

Key contract:
- Must call `default_mlops.log_metric()` for every metric computed.
- Document metrics and their significance in the class docstring.
- Should be deterministic given the same inputs.

## DAG eval_tasks

Add `eval_tasks` to a DAG to separate work from evaluation:

```python
from gluepy.exec import DAG
from .tasks import PrepareTask, TrainTask
from .eval_tasks import ComputeAccuracyTask

class ForecastDAG(DAG):
    label = "forecast"
    tasks = [PrepareTask, TrainTask]
    eval_tasks = [ComputeAccuracyTask]
```

- `eval_tasks` is optional. If omitted, the DAG has no evaluations.
- Evaluation tasks run after all work tasks, using the same run context.
- `inject_tasks()` appends eval tasks after work tasks by default.

## CLI Flags

```bash
# Full run (work + eval tasks)
python manage.py dag forecast

# Skip evaluation tasks
python manage.py dag forecast --skip-eval

# Run only evaluation tasks on an existing run
python manage.py dag forecast --eval-only --retry <run_folder>

# Compare metrics across runs
python manage.py dag forecast --compare <run_folder_1> <run_folder_2>
```

## Structured Metrics Output

After eval tasks run, the DAG runner prints a machine-readable block:

```
=== GLUEPY METRICS ===
metric:forecast_mape=12.5
metric:forecast_bias=-0.03
=== END METRICS ===
```

Metrics are also persisted to `metrics.json` in the run folder.

## Experiment Loop

Use the `/experiment` command (Claude Code) or `/experiment` (Cursor) to start an autonomous experiment loop:

```
/experiment forecast "improve the MAPE score"
```

The agent will iteratively modify work tasks, run the DAG, evaluate metrics, and keep/discard changes using git.
