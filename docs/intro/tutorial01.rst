=====================================
Writing your first Gluepy app, part 1
=====================================

Let's learn by writing a simple pipeline.

Throughout this tutorial, we'll walk you through how to setup a new Gluepy project
and how to leverage the various expects of Gluepy by writing a simple forecasting training
pipeline.

We'll assume that you already have :doc:`Gluepy installed </intro/install>` already. You can tell if Gluepy is installed with the following
execution in your terminal

.. parsed-literal::

    >>> import gluepy
    >>> print(gluepy.VERSION)
    |version|


If Gluepy is installed, you should see the version of your installation. The version you have installed may
be different from the version displayed above.


Creating a Project
==================

The first time you use Gluepy, you need to do some initial setup to get the
structure and files of your project in place. This is what is referred to as a 'Gluepy Project'
and it includes a :ref:`CLI entrypoint <cli>`, a set of :ref:`topic_settings` and a set of Gluepy :doc:`modules </topics/modules>`.

To create your project, go to a new directory where you want to store your code and run the following command:

.. code-block:: bash

   $ gluepy-cli startproject demo
   Created project 'demo'

This will create a ``demo/`` directory with the following structure:


* ``configs/``. The folder that contain all configurations in your application.

    * ``context.yaml``. The default parameters that populate your :ref:`context`.
    * ``settings.py``. The application parameters that populate your :doc:`Settings </ref/settings>`.

* ``manage.py``. The entrypoint to your project and the :ref:`CLI <cli>` from where you will execute your commands.

Next up, we want to create our first module that holds the logic of our application.


Create a Module
===============

Up until now, you have only created the minimal configuration required by a Gluepy project. None of the files you created
in the previous steps actually holds any business logic for your data pipelines.

Let's create our first :doc:`Module </topics/modules>`.

.. code-block:: bash

   $ python manage.py startmodule forecaster
   Created module 'forecaster'

This will create a new ``forecaster/`` directory within your project that holds the initial files
you will need for your Gluepy module in the following structure:

* ``dags.py``. This is the module that holds all your :ref:`dags` definitions.
* ``tasks.py``. This is the module that holds all your :ref:`tasks` definitions.

Both of these files can be replaced with directories named ``tasks/`` and ``dags/`` if your module grows to consist of many
:ref:`dags` and :ref:`tasks` that you want to separate into different files.


Install our Module
==================

To install and enable our module in our project, you need to go to the ``configs/settings.py`` file and add it to the :setting:`INSTALLED_MODULES`.

This will automatically import all the DAGs, Tasks and Commands defined in your module and expose it through the ``manage.py`` :ref:`cli`.


.. code-block:: python

   # settings.py
   INSTALLED_MODULES = ["forecaster", ]


Run our first DAG
=================

Now that we have created our project named ``demo``, added our first module named ``forecaster`` and activated it in our project,
let's ensure things are working correctly by running the ``SampleDAG`` defined to us by default in our ``dags.py`` file using the :ref:`cli_dag`.


.. code-block:: bash

   $ python manage.py dag sample
   INFO 2024-06-25 12:28:47,057 dag - ---------- Started task 'BootstrapTask'
   DEBUG 2024-06-25 12:28:47,057 tasks -
            Run ID: c24ef3e4-d869-427b-905e-8672caa4cd54
            Run Folder: runs/2024/6/25/c24ef3e4-d869-427b-905e-8672caa4cd54

   DEBUG 2024-06-25 12:28:47,058 local - Writing file to path '/demo/data/runs/2024/6/25/c24ef3e4-d869-427b-905e-8672caa4cd54/context.yaml'.
   INFO 2024-06-25 12:28:47,058 dag - ---------- Completed task 'BootstrapTask' in 0.001315 seconds
   INFO 2024-06-25 12:28:47,058 dag - ---------- Started task 'SampleTask'
   INFO 2024-06-25 12:28:47,058 dag - ---------- Completed task 'SampleTask' in 0.000001 seconds
