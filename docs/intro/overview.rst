==================
Gluepy at a glance
==================


Gluepy was developed by a team with a lot of experience in the fast-paced world of consulting,
and is designed to make development tasks fast and easy, with a structure that steer data scientists
into reusable, configurable patterns that can be put in production. Here's an informal overview of how
to create an AI and ML driven app using Gluepy.

The goal of this document is to give you enough technical specifics to
understand how Gluepy works, but this isn't intended to be a tutorial or
reference -- but we've got both! When you're ready to start a project, you can
:doc:`start with the tutorial </intro/tutorial01>` or :doc:`dive right into more
detailed documentation </topics/index>`.


.. _overview_dag:

Design your DAG (Pipeline)
##########################

.. code-block:: python

   from gluepy.exec import DAG, Task


   class SampleATask(Task):
       label = "sample_a"

       def run(self):
           print("Hello ")

   class SampleBTask(Task):
       label = "sample_b"

       def run(self):
           print("World!")


   class SampleDAG(DAG):
       label = "sample"
       tasks = [SampleATask, SampleBTask, ]


Next step, execute it!
----------------------

The DAG is automatically registered and available through :ref:`cli` and can be executed
with a single command.

.. code-block:: bash

   $ python manage.py dag sample
   Hello
   World!


.. _interact_with_data:

Load your DataFrames
####################

Gluepy provides a wrapper around any Dataframe backend of your choice (Pandas, Polars, PySpark etc) to ensure that
your project have consistency throughout in regards to file storages used, which path data is stored from,
automatic output versioning and safe usage of credentials.


.. code-block:: python

   import pandas as pd
   from gluepy.exec import Task
   from gluepy.files.data import data_manager


   class DataFrameTask(Task):
       label = "dataframe"

       def run(self):
           # Reading from /data/training.parquet
           df: pd.DataFrame = data_manager.read("training.parquet", root=True)
           df.loc[:, "new_column"] = 1

           # Automatically version output in unique run folder for this
           # current execution, since not defining ``root=True``.
           # /data/runs/2024/01/01/af41a763-18bc-44b0-9293-f52266898a89/training_v2.parquet
           data_manager.write("training_v2.parquet", df)


The ``data_manager`` object can be configured to point to any custom backend that may read in other types of
dataframes than Pandas as used in the example above, see :ref:`topic_data`.


.. _interact_with_filesystem:

Leverage File System API
########################

In a data driven project, there are more type of file interactions than just DataFrames. Gluepy comes with an exhaustive
API that allow you to interact with the file system in a cloud and SDK agnostic manner, which ensures that your code is
reusable, modular and can easily be deployed to use Local File System, Google Cloud Storage, S3 Bucket or other storage backends.


.. code-block:: python

   from io import StringIO
   from gluepy.exec import Task
   from gluepy.files.storages import default_storage


   class FileSystemTask(Task):
       label = "filesystem"

       def run(self):
           # Create a file
           data = default_storage.touch("file.txt", StringIO("Foo"))

           # Read a file
           data = default_storage.open("file.txt")

           # Delete a file
           default_storage.rm("file.txt")

           # Copy a file
           default_storage.cp("file.txt", "file2.txt")

           # List files and directories in path
           files, dirs = default_storage.ls(".")

           # Create a new directory
           default_storage.mkdir("tmp/")

           # Check if a path is a directory
           default_storage.isdir("tmp/")

           # Check if a path is a file
           default_storage.isfile("file.txt")

           # Check if a file exist
           default_storage.exists("file.txt")

The ``default_storage`` object can easily be configured to point to different file systems or storage backend
in case you want to run this code locally, on S3, GCS or other backends. See more on :ref:`topic_storage`.


.. _result_versioning_and_retry:

Version and recreate all output
###############################

As part of a ML/Data Science driven project, you may run your models hundreds of times with varying output
due to version of model used or :ref:`context` parameters defined for that particular execution.

Gluepy is designed to make it very easy to version the configuration and the output of a single execution
to ensure that the configuration used can be loaded later in time, and that output can be recreated.

This is all done using the concepts of :ref:`context_run_id` and :ref:`context_run_folder`.

The :ref:`context` is automatically serialized and stored in YAML format on every run, and any Dataframe is loaded and stored in the :ref:`context_run_folder`
without any need for any data scientist to define so explicitally.

These are the right, opinionated defaults to ensure that your project has the ability to recreate
previous output.


.. _configuration:

Extendability and configuration
###############################

Gluepy was built by a team with a rich experience of the AI Consulting world, which means that any code written must be able
to be deployed to various cloud environments and run with varying parameters that fit each client the best.

Gluepy comes with built in support for:

* :doc:`Modules </topics/modules/>` are reusable python packages that can be enabled in a project, and automatically loaded
  as part of the bootstrap process that registers the code and makes it available through the :ref:`cli`.
* :ref:`topic_settings` are global configuration of your project such as which modules that are enabled, how
  the logging configuration is defined, what credentials that are used to connect to data warehouse etc. Settings support
  :ref:`topic_settings_by_environment`.
* :ref:`topic_context` are model parameters that can be adjusted to impact the output or behavior of the execution, and
  other meta parameter around the execution used to be able to recreate any output.
* :ref:`storage_backends` are plug-and-play classes that adhere to Gluepy's predefined progammatic interfaces and
  provides logic to connect to the file system of your choice. You can easily create your own custom storage backend
  to work with your selected cloud provider.
* :ref:`data_backends` are plug-and-play classes that adhere to Gluepy's predefined progammatic interfaces and
  provides logic to load the data in the format of your choice. By default Gluepy comes with the
  ``PandasDataManager`` enabled, but you can easily write your own custom data backend that would return
  data as ``polars`` or ``pyspark`` dataframes.

  Gluepy is trying to strike the correct balance between being opinionated enough that steers data scientists
  towards best practices, while also allowing for configurability and extendability to ensure that AI Engineers have
  the ability to customize the behavior to deploy to their chosen technology stack and platform.
