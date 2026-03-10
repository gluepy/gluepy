=====================================
Writing your first Gluepy app, part 3
=====================================

In the previous parts of this tutorial :doc:`/intro/tutorial01` and :doc:`/intro/tutorial02` we have built a simple :ref:`dags` consisting of two :ref:`tasks`
that generate a set of data, and then fit an ``xgboost`` regressor on the data.

In this step, we will do the following:

* Parameterize the features used in the training of our machine learning mdoel using the :ref:`topic_context` to easily try new features without changing our code.
* Retry a pre-existing run to replicate our previous results.


Using Context Parameters
========================

As described in :ref:`topic_context`, the Context can be accessed using ``default_context``, and contains
the various configurations and parameters that should apply to our run, that by default is populated by the ``configs/context.yaml`` file.

This file is a sandbox where you and your team can store any parameter in YAML format that you may want to be able to tweak to adjust the behavior
of your :ref:`tasks`.

In our case, we'll use the context to parameterize the features used for training our ML model.


Let's customize our ``context.yaml`` file in the following manner:

.. code-block:: yaml

   meta:
       run_id:
       run_folder:
       created_at:

   forecaster:
       features: [article_id, date]


By adding the ``forecaster`` section above, we can access the features attribute in Python using
``default_context.forecaster.features``.

Now let's update our ``TrainingTask``.


.. code-block:: python

   import xgboost as xgb
   from gluepy.conf import default_context
   from gluepy.exec import Task
   from gluepy.files.data import data_manager
   import pandas as pd


   class TrainingTask(Task):
       label = "training"

       def run(self):
           df: pd.DataFrame = data_manager.read("training.csv")
           df["date"] = df["date"].astype("category")

           model = xgb.XGBRegressor(enable_categorical=True)
           # We update this row to refer to the columns to use as
           # features using the context attribute.
           model.fit(df[default_context.forecaster.features], df["units"])


This will now make it possible for our team to experiment and tweak the execution of
our machine learning pipeline by adjusting the YAML configuration instead of deploying new
versions of the code.


Loading an an existing Context
==============================

As you could see in the log output of :doc:`/intro/tutorial02`, each execution of our DAG will do the following:

* Assign a unique :ref:`context_run_id` to this training run of our model.
* Assign a unique :ref:`context_run_folder` to version and isolate the :ref:`context` and all our output.
* Gluepy automatically serialize and save our :ref:`context` to ``context.yaml`` within the run folder.
* Even though we only tell our code to read and write ``training.csv``, Gluepy automatically format the path to ``/demo/data/runs/2024/6/25/c29b8b49-dee9-4984-8ccc-860651780054/training.csv``

This makes it very easy to re-run a previous execution or configuration of your model to recreate results,
or inspect what parameters that were used to generate a given result.

For example, if your :ref:`context_run_folder` is ``runs/2024/6/25/c29b8b49-dee9-4984-8ccc-860651780054``, you will find a
file named ``context.yaml`` in the root of the directory which contains all the :ref:`topic_context` parameters used for that run,
and meta information such as the run id, run folder and timestamp of run execution.

The :ref:`cli_dag` support options such as ``--retry`` that allow you to retry a pre-existing run.


.. code-block:: bash

   $ python manage.py dag --retry runs/2024/6/25/c29b8b49-dee9-4984-8ccc-860651780054 sample
   DEBUG 2024-06-25 16:01:01,131 local - Reading file from path '/Users/lind.marcus/src/gluepy-tutorial/demo/data/runs/2024/6/25/c29b8b49-dee9-4984-8ccc-860651780054/context.yaml'.
   INFO 2024-06-25 16:01:01,132 dag - ---------- Started task 'BootstrapTask'
   DEBUG 2024-06-25 16:01:01,132 tasks -
            Run ID: c29b8b49-dee9-4984-8ccc-860651780054
            Run Folder: runs/2024/6/25/c29b8b49-dee9-4984-8ccc-860651780054

   DEBUG 2024-06-25 16:01:01,132 local - Writing file to path '/Users/lind.marcus/src/gluepy-tutorial/demo/data/runs/2024/6/25/c29b8b49-dee9-4984-8ccc-860651780054/context.yaml'.
   INFO 2024-06-25 16:01:01,133 dag - ---------- Completed task 'BootstrapTask' in 0.000831 seconds
   INFO 2024-06-25 16:01:01,133 dag - ---------- Started task 'GetTrainingDataTask'
   INFO 2024-06-25 16:01:01,134 pandas - Writing file to path 'runs/2024/6/25/c29b8b49-dee9-4984-8ccc-860651780054/training.csv'.
   DEBUG 2024-06-25 16:01:01,136 local - Writing file to path '/Users/lind.marcus/src/gluepy-tutorial/demo/data/runs/2024/6/25/c29b8b49-dee9-4984-8ccc-860651780054/training.csv'.
   INFO 2024-06-25 16:01:01,136 dag - ---------- Completed task 'GetTrainingDataTask' in 0.003068 seconds
   INFO 2024-06-25 16:01:01,136 dag - ---------- Started task 'TrainingTask'
   DEBUG 2024-06-25 16:01:01,136 local - Reading file from path '/Users/lind.marcus/src/gluepy-tutorial/demo/data/runs/2024/6/25/c29b8b49-dee9-4984-8ccc-860651780054/training.csv'.
   INFO 2024-06-25 16:01:01,136 pandas - Reading file from path 'training.csv'.
   INFO 2024-06-25 16:01:01,174 dag - ---------- Completed task 'TrainingTask' in 0.038568 seconds


Notice that instead of creating a new unique :ref:`context_run_id`, Gluepy is loading the ``context.yaml`` file in the path provided,
and reusing the same parameters and :ref:`context_run_folder`.

This ensures that the same parameters are being used as before, even if you code and default parameters have been changed since.


Retry subset of DAG
===================

In the step above, we showed you how to use ``--retry`` of the :ref:`cli_dag` to rerun a previous execution using the same :ref:`context_run_folder` and :ref:`topic_context`.

The :ref:`cli_dag` also support options such as ``--from-task`` and ``--task`` that does the same thing, but only retries a subset of the :ref:`dags`. This can be incredibly useful when you have
long running pipelines, and you want to skip sections of it and only rerun any :ref:`tasks` that you have changed.


.. code-block:: bash

   $ python manage.py dag --from-task training --retry runs/2024/6/25/c29b8b49-dee9-4984-8ccc-860651780054 sample
   DEBUG 2024-06-25 15:58:29,845 local - Reading file from path '/Users/lind.marcus/src/gluepy-tutorial/demo/data/runs/2024/6/25/c29b8b49-dee9-4984-8ccc-860651780054/context.yaml'.
   INFO 2024-06-25 15:58:29,845 dag - ---------- Started task 'TrainingTask'
   DEBUG 2024-06-25 15:58:29,845 local - Reading file from path '/Users/lind.marcus/src/gluepy-tutorial/demo/data/runs/2024/6/25/c29b8b49-dee9-4984-8ccc-860651780054/training.csv'.
   INFO 2024-06-25 15:58:29,846 pandas - Reading file from path 'training.csv'.
   INFO 2024-06-25 15:58:29,898 dag - ---------- Completed task 'TrainingTask' in 0.052679 seconds


Note that this time when we run our :ref:`dags`, we no longer execute the ``BootstrapTask`` or the ``GetTrainingDataTask`` but instead jump
to ``TrainingTask``. This execution will load the ``training.csv`` file that was generated the first time we executed this run.
