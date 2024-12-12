====
DAGs
====

The concept of workflows and pipelines that run a series of :ref:`topic_tasks` in a specific order can often be described as a :ref:`dags` (directed-acyclic-graph).
Given Gluepy is a framework to provide structure to your workflows, the concept of the :ref:`dags` is a primary citizen of the framework and a very core component.

Here is an example of a very simple Gluepy DAG:


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


This DAG can easily be executed using the :ref:`cli_dag`:


.. code-block:: bash

    python manage.py dag training



Orchestrating DAGs
==================

As described in the :doc:`Overview </intro/overview>`, Gluepy is **not** an orchestrator and is taking multiple steps to decouple
from what tools or architecture that is being used to actually execute the code. A Gluepy project should be able to be executed
on your Local Machine, `Airflow <https://airflow.apache.org/>`_, `Dagster <https://dagster.io/>`_ or other orchestrators.

This is achieved by the Gluepy :ref:`dags` format being agnostic to the various Orchestrator's DAG formats, and you can
create CLI commands such as :ref:`cli_airflow_generate` to translate the Gluepy DAG into an Airflow DAG using Jinja templating.

The benefit of this is that your broader Data Science or Machine Learning team do not need to be familiar with the architecture
or tools involved to run their pipelines in production, and instead there can be a separation of concern between the Data Scientists
and the Engineers on topics such as Scheduling, Orchestration, Horizontal Scaling and so on.


.. _topic_tasks:

Tasks
=====

A :ref:`tasks` is the class that holds the actual logic of a step in your :ref:`dags`. This is where you read in data, write custom code,
transform your dataframes and train your machine learning models.

Because of the distinction between a :ref:`dags` and a :ref:`tasks`, a :ref:`tasks` can be reused across multiple :ref:`dags`. The task itself is not
aware or coupled to any specific DAG.


Here is an example Task that we wrote in :doc:`/intro/tutorial02`

.. code-block:: python

   import os
   import io
   import pickle
   import xgboost as xgb
   from gluepy.exec import Task
   from gluepy.conf import default_context
   from gluepy.files.data import data_manager
   from gluepy.files.storages import default_storage
   import pandas as pd


   class TrainingTask(Task):
       label = "training"

       def run(self):
           # Read the training dataset previous generated in
           # ``GenerateTrainingDataTask``. The path is automatically
           # formatted to read from the run_folder to ensure data versioning
           # and isolation of output between executions.
           df: pd.DataFrame = data_manager.read("training.csv")
           df["date"] = df["date"].astype("category")

           # Train our machine learning model.
           model = xgb.XGBRegressor(enable_categorical=True)
           model.fit(df[["date", "article_id"]], df["units"])

           # Store model to disk to later be used when we want
           # to do inference.
           stream = io.BytesIO()
           pickle.dump(model, stream)
           stream.seek(0)
           default_storage.touch(
               os.path.join(default_context.gluepy.run_folder, "model.pkl"), stream
           )


Passing objects between Tasks
-----------------------------

The ``run()`` method is the entrypoint to any :ref:`tasks`, and you may notice that ``run()`` do not accept any keyword argument
being passed into it. This is an intentional design choice to avoid data scientists building in-memory dependencies between tasks
that make it very challenging to try subset of a :ref:`dags`, or orchestrate your various tasks in parallel across a cluster of machines
that do not share memory.

The preferred way to pass data between a series of :ref:`tasks` is to simply write to disk using the ``default_storage`` object as described
in :ref:`topic_storage`, and load it from disk in the next step.

This ensures that if a step fail, it can be retried without re-running the full :ref:`dags`.
