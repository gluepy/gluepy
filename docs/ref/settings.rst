========
Settings
========

.. contents::
    :local:
    :depth: 1

Gluepy have two types of configurations, we have the :ref:`core_settings` that contains our "Project" configuration such as
connection details, logging configuration, installed modules, and we also have the :ref:`context_configuration` which refers to the specific
model parameters of the execution our DAG, its ``run_id``, ``run_folder`` and so on.


.. _core_settings:

Core Settings
=============

The core settings are the project settings that are automatically loaded for any execution happening with the ``manage.py`` :ref:`cli`.
These configurations can be environment specific, and you can refer which settings to load using the ``GLUEPY_SETTINGS_MODULE`` environment variable.


.. setting:: BASE_DIR

``BASE_DIR``
------------

Default: ``os.path.dirname(os.path.dirname(__file__))`` (path to root of project)

A string that represent the full absolute path to the root of the project, used
by other settings and configuration to construct paths.


.. setting:: CONFIG_PATH

``CONFIG_PATH``
---------------

Default: ``os.path.join(BASE_DIR, "configs")`` (path to configs folder of project)

A string that represent the full absolute path to the configs folder of the project where your 
YAML files resides that later populate your default :ref:`context`.



.. setting:: INSTALLED_MODULES

``INSTALLED_MODULES``
---------------------

Default: ``[]`` (empty list of strings)

A list of strings that represent the dotted import path available on your system path for any Gluepy module that you want to enable as part of the project.

See more at :doc:`Reusable Apps </intro/reusable-apps>`.


.. setting:: STORAGE_ROOT

``STORAGE_ROOT``
----------------

Default: ``os.path.join(BASE_DIR, "data")`` (file path to data directory)

The path to the root of where all data assets are located. This path could be an absolute local path if using the ``LocalStorage`` :setting:`STORAGE_BACKEND` or
it can be a relative path of using Blob Storage backends such as ``S3Storage``.


.. setting:: STORAGE_BACKEND

``STORAGE_BACKEND``
-------------------

Default: ``"gluepy.files.storages.LocalStorage"`` (dotted string to ``LocalStorage``)

Dotted path to the :ref:`storage_backends` class to be loaded and later used by the ``default_storage`` object throughout application.
.. setting:: DATA_BACKEND

``DATA_BACKEND``
-------------------

Default: ``"gluepy.files.data.PandasDataManager"`` (dotted string to ``PandasDataManager``)

Dotted path to the :ref:`data_backends` class to be loaded and later used by the ``data_manager`` object throughout application.



.. setting:: CONTEXT_BACKEND

``CONTEXT_BACKEND``
-------------------

Default: ``"gluepy.conf.context.DefaultContextManager"`` (dotted string to ``DefaultContextManager``)

Dotted path to the :ref:`context_configuration` manager class to be loaded and later used by the ``default_context`` object throughout application.



.. setting:: START_TASK

``START_TASK``
-------------------

Default: ``"gluepy.exec.tasks.BootstrapTask"`` (dotted string to ``BootstrapTask``)

Dotted path to a :ref:`task` that we want to inject to the beginning of every DAG that we execute in our project.
Usually helpful to provide a standard set of diagnostic meta data around the execution.

.. setting:: LOGGING

``LOGGING``
-------------------

Default: ``{}`` (empty dictionary)

A ``logging.dictConfig`` that is loaded for any command executed through the :ref:`cli`.



.. _context_configuration:

Context Configuration
=====================

As described in detail in our :doc:`Context topic guide </topics/context>`, the Context Configuration refers to the DAG/Model specific
parameters that made up a specific execution, that you may want to frequently adjust to tweak the behavior of your pipeline and project.

Unlike the :ref:`core_settings` which are standardize and predefined, the Context is more of a "user config" where you can add any parameter
or variable that you may want to use throughout your project.

For example, you may have a ``context.yaml`` file that looks like this:


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



.. _context:

Context
-------

Singleton class that holds all parameters and configurations related to the specific execution, such as ``run_id``, ``run_folder``, ``created_at`` and other project parameters.
The context is lazily evaluated using the :ref:`context_manager` and accessible using the ``gluepy.conf.default_context`` object. 

Given its a singleton, there can only accept a single instance of a ``Context`` at any point in time.

.. autoclass:: gluepy.conf.context.Context
    :members:

.. _context_manager:

Context Managers
----------------

The ``default_context`` object is automatically populated using the backend defined in :setting:`CONTEXT_BACKEND`. This allow you
as a developer to extend Gluepy to potentially create your own class that may load parameters from a remote source, an API, an environment variable
or from any other sources.

Gluepy comes with a ``DefaultContextManager`` out of the box that loads the ``default_context`` from .yaml files located in the :setting:`CONFIG_PATH` directory.

If you ever need to access the instance of the :setting:`CONTEXT_BACKEND` context manager directly, you can do so using the lazily evaluated ``gluepy.conf.default_context_manager`` object.

.. autoclass:: gluepy.conf.context.DefaultContextManager
    :members:


Protected Parameters
--------------------

There are a few parameters that are populated by Gluepy, these are defined under the ``meta`` tag and contain meta data around the ongoing execution.

.. code-block:: yaml

   meta:
    run_id:
    run_folder:
    created_at:
