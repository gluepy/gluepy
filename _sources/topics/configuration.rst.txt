=============
Configuration
=============

.. _topic_settings:

Settings
========

As described in :doc:`Settings Reference </ref/settings>`, Gluepy have two types of settings made up of the :ref:`context` and
:doc:`Settings </ref/settings>`.

The Settings is the application / project wide application settings for the environment you are currently executing your code on. These
settings include what modules you have activated, which logging configuration you have, any references to credentials required to
connect to your data warehouse and more.


.. _topic_settings_by_environment:

Different Settings by Environment
---------------------------------

A common use case would be to have different project settings for different environments. For example, you may
want to use different settings for your local development versus your production workloads. This can be done by
splitting the ``settings.py`` file into multiple files by environment, and pointing to the one you want to enable
as a dotted string path with the ``GLUEPY_SETTINGS_MODULE`` environment variable.

For example, you may have the following settings:

- src/

  - configs/

    - base.py
    - prod.py
    - ...
  - myapp/
  - manage.py



.. code-block:: python

   # base.py
   STORAGE_BACKEND = "gluepy.files.storages.local.LocalStorage"
   STORAGE_ROOT = os.path.join(BASE_DIR, "data")
   LOGGING = {
      'version': 1,
      'disable_existing_loggers': False,
      'formatters': {
          'simple': {
              'format': '{levelname} {asctime} {module} - {message}',
              'style': '{'
          }
      },
      'handlers': {
          'stream': {
              'level': 'DEBUG',
              'class': 'logging.StreamHandler',
              'formatter': 'simple',
          }
      },
      'loggers': {
          'gluepy': {
              'handlers': ['stream', ],
              'level': 'DEBUG',
              'propagate': True,
          },
       }
   }


.. code-block:: python

   # prod.py
   from .base import *
   STORAGE_BACKEND = "gluepy.files.storages.google.GoogleStorage"
   STORAGE_ROOT = "data/"
   GOOGLE_GCS_BUCKET = "mybucket-1234"

Then set an environment variable on your system named ``GLUEPY_SETTINGS_MODULE`` to ``configs.prod``.
All commands executed with ``manage.py`` will now load the ``prod.py`` settings using ``base.py`` as the defaults.


.. _topic_context:

Context
=======

In the exploratory, experimental, scienticic world of Data Science and Machine Learning, it is crucial to be able to modify
the behavior of your pipeline or model without changing significant amount of code. E.g. you may want to change the dates
used to train your model, the features used or other parameters.

The :ref:`context` is a singleton object that is instantiated in the beginning of each execution of your pipeline, and populated
with various parameters and configurations that is specific to that execution.

The context of a run is always serialized and store together with the :ref:`context_run_folder` to ensure that you can
rerun and replicate the output of a historical/previous execution of a DAG.


.. _context_default_context:

Default Context Object
----------------------

The ``default_context`` object is the lazily evaluated object that holds the :ref:`context` of your execution, and where you can
access all your parameters from within your code.

Your default parameters are defined in ``.yaml`` files stored within the :setting:`CONFIG_PATH` directory and are automatically populated
by the :ref:`context_manager`.

For example, you may have a ``config.yaml`` file that looks like this

.. code-block:: yaml

   # Gluepy protected parameters
   meta:
    run_id:
    run_folder:
    created_at:

   # Custom user added parameters
   forecaster:
    start_date: 2024-01-01


That you later want to access in your Python code like this:


.. code-block:: python

    from gluepy.conf import default_context
    from gluepy.exec import Task


    class ForecasterTask(Task):

        def run(self):
          print(default_context.forecaster.start_date)


If in the future, you change your ``config.yaml`` file, you can still rerun and replicate the same results using the same parameters
as defined in :ref:`context_retry_example`.


.. _context_run_id:

Run ID
------

The Run ID is a unique identifier that is given to the specific execution/run that you are running.
This ID is assigned in the ``DefaultContextManager`` defined in :setting:`CONFIG_BACKEND` and defaults to a ``uuid4``.

If you want to customize the default run ID, you can create your own ``ContextManager`` and refer to it in :setting:`CONFIG_BACKEND`.


.. code-block:: python

    from gluepy.conf import default_context
    from gluepy.exec import Task


    class ForecasterTask(Task):

        def run(self):
          print(default_context.forecaster.meta.run_id)


.. _context_run_folder:

Run Folder
----------

To ensure the ability to replicate results of a previous run, and to ensure that output of your pipeline is
versioned, each execution of Gluepy use the :ref:`context_run_id` to create a directory on your :ref:`storage_backends`
that is unique to the specific run, where it can serialize and save the :ref:`context`, and any other input or output.

.. code-block:: python

    from gluepy.conf import default_context
    from gluepy.exec import Task


    class ForecasterTask(Task):

        def run(self):
          # /runs/2024/01/01/af41a763-18bc-44b0-9293-f52266898a89/
          print(default_context.forecaster.meta.run_folder)


By default, all paths used with the data managers are relative to the ``run_folder``. Any time you want to reach out outside of the Run's ``run_folder`` you
need to do so explicitally using the ``root`` kwarg.


.. code-block:: python

    import pandas as pd
    from gluepy.conf import default_context
    from gluepy.files.data import data_manager
    from gluepy.exec import Task


    class ForecasterTask(Task):

        def run(self):
          # Writes to /runs/2024/01/01/af41a763-18bc-44b0-9293-f52266898a89/file.csv
          data_manager.write("file.csv", pd.DataFrame({"foo": [1]}))

          # Writes to /file.csv
          data_manager.write("file.csv", pd.DataFrame({"foo": [1]}), root=True)


.. _context_retry_example:

Retry previous run
------------------

.. warning::

    Retrying a run will reuse the same ``run_folder`` and ``run_id``, which means that the execution would
    overwrite any previous output.


Since the :ref:`context` is serialized and stored in the :ref:`context_run_folder` automatically on each run, and all
data by default is saved within a run's :ref:`context_run_folder`, Gluepy makes it very easy to re-run and replicate the output
of a previous execution.

This is done using the :ref:`cli_dag` and the ``-retry`` option.

.. code-block:: bash

    $ python manage.py dag forecaster --retry /runs/2024/01/01/af41a763-18bc-44b0-9293-f52266898a89/

You can also retry a previous run but start from a specific task that is not the beginning using the ``--from-task`` option.

.. code-block:: bash

    $ python manage.py dag forecaster --from-task training --retry /runs/2024/01/01/af41a763-18bc-44b0-9293-f52266898a89/
