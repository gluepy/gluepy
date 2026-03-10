=======
Modules
=======

Gluepy have the ability to automatically load and activate reusable modules that you can use between projects. These modules
may contain DAG's, Tasks or CLI Commands that you want to be exposed through the :doc:`Command Line Interface (CLI) </ref/cli>`.


.. _topic_modules:

Activate a Gluepy Module
========================

Activating a Gluepy module is done using the :setting:`INSTALLED_MODULES` setting. You are supposed to give the dotted import path available on your system
to the given module that you want to activate.

When defining a module in :setting:`INSTALLED_MODULES`, Gluepy will automatically import all Tasks, DAGs and Commands during bootstrapping
as long as they are available in ``<module>.tasks``, ``<module>.dags``, ``<module>.commands`` import paths.

.. code-block:: python

    INSTALLED_MODULES = [
        "companyutils",
        "myforecaster",
    ]
