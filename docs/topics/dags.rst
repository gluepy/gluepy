====
DAGs
====

The concept of workflows and pipelines that run a series of :ref:`tasks` in a specific order can often be described as a :ref:`dags` (directed-acyclic-graph).
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
