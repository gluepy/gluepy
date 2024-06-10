====
Data
====

Data interactions is a key component of any project that leverage Gluepy. As a technology agnostic framework, we intend to make Gluepy flexible
for you to customize and configure to work with what ever your data technology stack of choice is, and no matter which cloud provider you are using.

This file describes some of the features that might be relevant to Gluepy
usage. It is not intended as a replacement for server-specific documentation or
reference manuals.

General notes
=============

.. _separate_data_from_storage:

Separate Dataframes from Storage
--------------------------------

When it comes to interacting with data, Gluepy are separating the various kind of actions into two types of actions,
the "File system actions" such as listing directories, creating files, checking paths and so on is managed by the :ref:`storage_backends`.
While the "dataframe" reads and writes are managed by the :ref:`data_backends`.

This means that you can separately define if you are using Local filesystem, S3 file system or Google Storage file system, from if you are using Pandas, Polars or PySpark
in your project.


.. _storage_backends:

Storage Backends
================

As described in our :doc:`Storages Topic guide </topics/storages>`, all file interactions such as creating directories, checking for file existance, creating files or reading files are done using 
the ``default_storage`` object. This object is lazily evaluated at runtime to whatever :ref:`storage_backends` defined in :setting:`STORAGE_BACKEND`.

This means that by using ``default_storage`` and modifying :setting:`STORAGE_BACKEND` in your project, you can use the same code or libraries on multiple
file systems simply by adjusting your configuration.

By default, Gluepy comes included with the following :setting:`STORAGE_BACKEND` support:

* :ref:`storage_backend_local`
* :ref:`storage_backend_google`
* :ref:`storage_backend_s3`


.. _storage_backend_local:

The LocalStorage Class
----------------------

The ``LocalStorage`` class is the storage implementation that use the local file system, and is used by Gluepy as a default :setting:`STORAGE_BACKEND` when you start a new project.
The ``LocalStorage`` backend is based on the interface and methods defined on :ref:`storage_backend_base`.


.. _storage_backend_google:

The GoogleStorage Class
-----------------------

The ``GoogleStorage`` class is the storage implementation that use `GoogleStorage <https://cloud.google.com/storage>`_ as a file system. It is based on the interface and methods defined on :ref:`storage_backend_base`.

The class is a wrapper around the `google-cloud-storage <https://pypi.org/project/google-cloud-storage/>`_ PyPI package and is able to use the same authentication methods as defined in `Google Documentation <https://cloud.google.com/docs/authentication/client-libraries>`_.

Custom Settings
~~~~~~~~~~~~~~~

* ``GOOGLE_GCS_BUCKET`` define the name of the GoogleStorage bucket that you want to use.

Use :setting:`STORAGE_ROOT` to define where on bucket files are stored, this setting should be set to a relative path on the bucket. E.g. ``"my_project/data/"``.


.. _storage_backend_s3:

The S3Storage Class
-------------------

.. warning::

    The S3Storage is partly implemented and is currently missing some implementations such as ``cp()``, ``isdir()`` and ``isfile()``.


The ``S3Storage`` class is the storage implementation that use `S3 <https://aws.amazon.com/s3/>`_ as a file system. It is based on the interface and methods defined on :ref:`storage_backend_base`.

The class is a wrapper around the `boto3 <https://pypi.org/project/boto3/>`_ PyPI package and is able to use Access Key and Access Secret Key as authentication method.

Custom Settings
~~~~~~~~~~~~~~~

* ``AWS_S3_REGION_NAME`` defines the AWS region to use. E.g. ``"eu-west-1"``.
* ``AWS_S3_ENDPOINT_URL`` custom S3 URL to use when connecting to S3, including scheme.
* ``AWS_ACCESS_KEY_ID`` AWS Access Key to be used for authentication together with ``AWS_SECRET_ACCESS_KEY``.
* ``AWS_SECRET_ACCESS_KEY`` AWS Secret Key to be used for authentication together with ``AWS_ACCESS_KEY_ID``.
* ``AWS_STORAGE_BUCKET_NAME`` name of the S3 bucket to connect to.

Use :setting:`STORAGE_ROOT` to define where on bucket files are stored, this setting should be set to a relative path on the bucket. E.g. ``"my_project/data/"``.


.. _storage_backend_base:

The BaseStorage Class
---------------------

The ``BaseStorage`` class is the default interface that define the required methods and arguments for any storage implementation.
This is an abstract class that raise ``NotImplementedError`` on use, but is used by :ref:`storage_backend_local` and other storage backends
to ensure consistency.


.. autoclass:: gluepy.files.storages.BaseStorage
    :members:



.. _data_backends:

Data Backends
=============

As described in our :doc:`Data Topic guide </topics/data>`, all dataframe read and writes are done using 
the ``data_manager`` object. This object is lazily evaluated at runtime to whatever :ref:`data_backends` defined in :setting:`DATA_BACKEND`.

This means that by using ``data_manager`` and modifying :setting:`DATA_BACKEND` in your project, you can customize the behavior of Gluepy and work
with your prefered ways of dataframe technologies such as Polars, PySpark or Pandas.

By default, Gluepy comes included with the following :setting:`DATA_BACKEND` support:

* :ref:`data_backend_pandas`


.. _data_backend_pandas:

The PandasDataManager Class
----------------------

The ``PandasDataManager`` class is the data manager implementation that use interacts with `Pandas Dataframes <https://pypi.org/project/pandas/>`_, and is used by Gluepy as a default :setting:`DATA_BACKEND` when you start a new project.
The ``PandasDataManager`` backend is based on the interface and methods defined on :ref:`data_backend_base`.


.. _data_backend_base:

The BaseDataManager Class
-------------------------

The ``BaseDataManager`` class is the default interface that define the required methods and arguments for any data manager implementation.
This is an abstract class that raise ``NotImplementedError`` on use, but is used by :ref:`data_backend_pandas` and other data manager backends
to ensure consistency.

.. autoclass:: gluepy.files.data.BaseDataManager
    :members:
