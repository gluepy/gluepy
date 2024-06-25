=====================================
Writing your first Gluepy app, part 2
=====================================

In the previous step :doc:`/intro/tutorial01`, we setup our Project, created our ``forecaster`` module, and tried running our first ``SampleDAG``.
Next up, we will write some of our own code that introduce the topics of how Gluepy help you accessing your data by writing a simple forecaster training step.

In this tutorial we will:

* Create a ``GetTrainingDataTask`` that generate some sample training data for us.
* Create a ``TrainingTask`` that use ``xgboost`` to train a regression model.


Generate Training Data
======================


The first step we want to do is to modify our ``forecaster/tasks.py`` file and add the following class:


.. code-block:: python

   from datetime import datetime
   from gluepy.exec import Task
   from gluepy.files.data import data_manager
   import pandas as pd


   class GetTrainingDataTask(Task):
       label = "get-data"

       def run(self):
           """Entrypoint to our task"""
           # Generating a sample dataframe to later
           # be used for training. In a real project
           # you would likely instead read data from a
           # pre-existing dataset.
           df = pd.DataFrame({
               "units": [10, 5, 3, 11, 8],
               "date": [
                    datetime(2024, 1, 1),
                    datetime(2024, 1, 2),
                    datetime(2024, 1, 3),
                    datetime(2024, 1, 4),
                    datetime(2024, 1, 5)
               ],
               "article_id": [1, 1, 1, 1, 1]
           })

           # Write dataset to run_folder.
           data_manager.write("training.csv", df, index=False)


This does a few simple things:

* Define a new :ref:`tasks` instance where the business logic lives in the ``run()`` method.
* Generate mock data as a Pandas Dataframe that will later be used for training.
* Use the :ref:`data_manager <topic_data>` to store the dataframe in the run's :ref:`context_run_folder`.


Next up, we need to add this new :ref:`tasks` to our ``SampleDAG`` within our ``forecaster/dags.py`` file.


.. code-block:: python

   from gluepy.exec import DAG
   from .tasks import GetTrainingDataTask


   class SampleDAG(DAG):
       label = "sample"
       tasks = [GetTrainingDataTask]


Now let's try running our ``SampleDAG`` again with the :ref:`cli_dag` to ensure it is still working.


.. code-block:: bash

   $ python manage.py dag sample
   INFO 2024-06-25 12:48:44,061 dag - ---------- Started task 'BootstrapTask'
   DEBUG 2024-06-25 12:48:44,062 tasks -
            Run ID: e7966509-ca8f-4e12-8c9f-7b0b1c2fcfd4
            Run Folder: runs/2024/6/25/e7966509-ca8f-4e12-8c9f-7b0b1c2fcfd4

   DEBUG 2024-06-25 12:48:44,062 local - Writing file to path '/demo/data/runs/2024/6/25/e7966509-ca8f-4e12-8c9f-7b0b1c2fcfd4/context.yaml'.
   INFO 2024-06-25 12:48:44,062 dag - ---------- Completed task 'BootstrapTask' in 0.000991 seconds
   INFO 2024-06-25 12:48:44,062 dag - ---------- Started task 'GetTrainingDataTask'
   INFO 2024-06-25 12:48:44,064 pandas - Writing file to path 'runs/2024/6/25/e7966509-ca8f-4e12-8c9f-7b0b1c2fcfd4/training.csv'.
   DEBUG 2024-06-25 12:48:44,102 local - Writing file to path '/demo/data/runs/2024/6/25/e7966509-ca8f-4e12-8c9f-7b0b1c2fcfd4/training.csv'.
   INFO 2024-06-25 12:48:44,102 dag - ---------- Completed task 'GetTrainingDataTask' in 0.039749 seconds


Training our Machine Learning Model
===================================

Next up, it is time to create our ``TrainingTask``. First, we must first install some additional dependencies that we will use to train our
machine learning model.

.. code-block:: bash

   $ pip install scikit-learn xgboost


After installing ``xgboost`` and ``scikit-learn`` we can create our ``TrainingTask`` class.


.. code-block:: python

   import xgboost as xgb
   from gluepy.exec import Task
   from gluepy.files.data import data_manager
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

We must then add our new ``TrainingTask`` to our ``SampleDAG``:

.. code-block:: python

   from gluepy.exec import DAG
   from .tasks import GetTrainingDataTask, TrainingTask


   class SampleDAG(DAG):
       label = "sample"
       tasks = [GetTrainingDataTask, TrainingTask]


Finally, we can try executing our updated ``SampleDAG`` using the :ref:`cli_dag`.

.. code-block:: bash

   $ python manage.py dag sample
   INFO 2024-06-25 13:10:37,903 dag - ---------- Started task 'BootstrapTask'
   DEBUG 2024-06-25 13:10:37,903 tasks -
            Run ID: c29b8b49-dee9-4984-8ccc-860651780054
            Run Folder: runs/2024/6/25/c29b8b49-dee9-4984-8ccc-860651780054

   DEBUG 2024-06-25 13:10:37,904 local - Writing file to path '/demo/data/runs/2024/6/25/c29b8b49-dee9-4984-8ccc-860651780054/context.yaml'.
   INFO 2024-06-25 13:10:37,904 dag - ---------- Completed task 'BootstrapTask' in 0.001035 seconds
   INFO 2024-06-25 13:10:37,904 dag - ---------- Started task 'GetTrainingDataTask'
   INFO 2024-06-25 13:10:37,905 pandas - Writing file to path 'runs/2024/6/25/c29b8b49-dee9-4984-8ccc-860651780054/training.csv'.
   DEBUG 2024-06-25 13:10:37,906 local - Writing file to path '/demo/data/runs/2024/6/25/c29b8b49-dee9-4984-8ccc-860651780054/training.csv'.
   INFO 2024-06-25 13:10:37,906 dag - ---------- Completed task 'GetTrainingDataTask' in 0.002413 seconds
   INFO 2024-06-25 13:10:37,906 dag - ---------- Started task 'TrainingTask'
   DEBUG 2024-06-25 13:10:37,906 local - Reading file from path '/demo/data/runs/2024/6/25/c29b8b49-dee9-4984-8ccc-860651780054/training.csv'.
   INFO 2024-06-25 13:10:37,906 pandas - Reading file from path 'training.csv'.
   INFO 2024-06-25 13:10:37,945 dag - ---------- Completed task 'TrainingTask' in 0.038396 seconds


Note the following:

* Gluepy automatically assign a unique :ref:`context_run_id` to this training run of our model.
* Gluepy automatically assign a unique :ref:`context_run_folder` to version and isolate the :ref:`context` and all our output.
* Gluepy automatically serialize and save our :ref:`context` to ``context.yaml`` within the run folder.
* Even though we only tell our code to read and write ``training.csv``, Gluepy automatically format the path to ``/demo/data/runs/2024/6/25/c29b8b49-dee9-4984-8ccc-860651780054/training.csv``


We have now created a set of custom :ref:`tasks` instances that use the ``data_manager`` object and :ref:`topic_data` to read and write data. Next up we will see how we can use :ref:`context` to parameterize our project and make it easier to configure in the future.
