====
Data
====

Data is of course a key part of any machine learning or data science project, and Gluepy comes packaged with multiple
helpful tools to help read, interact and customize any data interaction.

.. _topic_storage:

Storage and File System
=======================

All file system interaction should be done using the ``default_storage`` object which is instantiated with the class defined in :setting:`STORAGE_BACKEND`. The ``default_storage`` object have the methods defined as described on :ref:`storage_backend_base`.

By using the ``default_storage`` object, you do not need to be concerned if you are on Azure, GCP, S3 or your local file system. Your code looks the same and migrating from
local development, to production workloads in the cloud is as easy as changing the :setting:`STORAGE_BACKEND` setting.


.. code-block:: python

    from gluepy.exec import Task
    from gluepy.files.storages import default_storage


    class ForecasterTask(Task):

        def run(self):
            if default_storage.exists("file.txt"):
                data = default_storage.open("file.txt")
            else:
                raise FileNotFoundError("file.txt not found")


Use Cloud Storage
-----------------

By default, :setting:`STORAGE_BACKEND` points to the :ref:`storage_backend_local`. This makes it easy for you to get started with Gluepy on your local machine.

Many project may have data that cannot fit into the local machine or your business may have a centralized data lake where all data resides. For these situations, you must
change the :setting:`STORAGE_BACKEND` to point to a :ref:`storage_backends` that support your cloud storage of choice.

Gluepy already support the following providers:

* :ref:`storage_backend_local`
* :ref:`storage_backend_google`
* :ref:`storage_backend_s3`

Here is an example using the :ref:`storage_backend_google`.


.. code-block:: python

    # settings.py
    STORAGE_BACKEND = "gluepy.files.storages.GoogleStorage"
    GOOGLE_GCS_BUCKET = "mybucket-1234"


Now, my ``default_storage`` object will point to an instance of ``GoogleStorage``, and all method calls will authenticate to Google Cloud Storage and
use it as a file system for our Gluepy project.

.. _topic_data:

Data and DataFrames
===================

All reads and writes of DataFrames should be done using the ``data_manager`` object. This object is lazily evaluated to the :setting:`DATA_BACKEND`, which allow you to
modify what kind of data frame that is returned with minor changes to your code.

The benefit of ensuring that your project use the ``data_manager`` instead of reading the data directly, is that it will ensure that all your Dataframes are stored and versioned in the :ref:`context_run_folder`, and
it will automatically read the data from the :setting:`STORAGE_BACKEND` defined.

You may want to work with Spark DataFrames, Polars Dataframes or Pandas Dataframes. If you want to modify the type of data frame that your project is relying on,
you can change that using the :setting:`DATA_BACKEND`.

See :ref:`data_backends` for the currently supported providers.


.. code-block:: python


    from gluepy.exec import Task
    from gluepy.files.data import data_manager


    class ForecasterTask(Task):

        def run(self):
            df = data_manager.read("training.parquet")


.. _topic_data_validation:

Schemas and Data Validation
---------------------------

There are plenty of great DataFrame validation frameworks out there, and we have made the decision to not invent our own. We recommend that you use
tools such as `pandera <https://pandera.readthedocs.io/en/stable/>`_ or `pydantic <https://docs.pydantic.dev/latest/>`_ to do your data validation.

.. code-block:: python


    from datetime import datetime
    from gluepy.exec import Task
    from gluepy.files.data import data_manager
    import pandera as pa


    class TrainingSchema(pa.DataFrameModel):
        created_at: pa.typing.Series[datetime]
        article_id: pa.typing.Series[int]
        store_id: pa.typing.Series[int]
        units_sold: pa.typing.Series[int]


    class ForecasterTask(Task):

        def run(self):
            df = TrainingSchema(data_manager.read("training.parquet"))
