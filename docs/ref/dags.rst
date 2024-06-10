=============================
Directed Acyclic Graphs (DAG)
=============================

As a framework that structures workflows and pipelines, Gluepy's key components are the :ref:`dags` and :ref:`tasks`.
A ``DAG`` is your directed-acyclic-graph, or "pipeline" and its made up of one or more ``Task`` instances that holds the
logic of that step in your pipeline.

.. _dags:

DAG
===

.. autoclass:: gluepy.exec.dags.DAG
    :members:


.. code-block:: python

    from gluepy.exec import DAG
    from .tasks import (
        DataTask, ForecastTrainingTask, ForecastTestTask, OutputFormatTask
    )


    class TrainingDAG(DAG):
        label = "training"
        tasks = [
            DataTask, ForecastTrainingTask, ForecastTestTask, OutputFormatTask
        ]


.. _dags_registry:

DAG Registry
------------

All DAGs that are part of a module registered in :setting:`INSTALLED_MODULES` will automatically be added to the DAG Registry located at
``gluepy.exec.dags.REGISTRY``. This ``REGISTRY`` is the source of truth of all available DAGs that is available to run through the :ref:`cli` and the
:ref:`cli_dag`.


.. _tasks:

Task
====

A ``Task`` is a single step in a :ref:`dags`, and holds the logic and code related to that step. It has an entrypoint method ``run()`` that must be
defined as part of a ``Task`` to not raise an error.

Tasks intentionally do not accept any keyword arguments in the ``run()`` method, this is to ensure that every ``Task`` in your ``DAG`` do not have
in-memory dependencies from previous ``Task`` earlier in the ``DAG``, and that each ``Task`` can be retried independently at failure without the 
need to rerun the full ``DAG``.

.. autoclass:: gluepy.exec.tasks.Task
    :members:


.. code-block:: python

    from gluepy.exec import Task
    from gluepy.files.data import data_manager


    class ForecastTrainingTask(Task):
        label = "forecast-training"

        def run(self):
            """Entrypoint to our task"""
            df = data_manager.read("training.parquet")
            # Add additional logic to train model...


.. _tasks_registry:

Task Registry
-------------

All Tasks that are part of a module registered in :setting:`INSTALLED_MODULES` will automatically be added to the Task Registry located at
``gluepy.exec.tasks.REGISTRY``. This ``REGISTRY`` is the source of truth of all available Tasks that is available to run through the :ref:`cli` and the
:ref:`cli_dag`.
