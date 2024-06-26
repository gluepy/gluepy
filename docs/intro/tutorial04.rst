=====================================
Writing your first Gluepy app, part 4
=====================================

In the previous parts of this tutorial :doc:`/intro/tutorial01`, :doc:`/intro/tutorial02` and :doc:`/intro/tutorial03` we have setup
a project that contains a :ref:`dags` that train a machine learning model on some sample data.

Next up, we'll talk about the CLI and commands.

Gluepy already comes bundled with pre-existing commands that allow you to do basic tasks such as running your :ref:`dags`
with the :ref:`cli_dag`, but there may be situations where you want to add functionality or scripts to your project that
does not fit into the concept of a :ref:`dags` or :ref:`tasks`. E.g. you may want to write a command that copies a run folder,
or a command that takes a trained .pkl model file and deploys it in a registry.

In this final step of the tutorial, we will introduce the concept of writing custom :ref:`cli` that copies the output of a previous
run to a new location, to simulate a deployment to production.


Reviewing the default CLI command
=================================

If you recall :doc:`/intro/tutorial01`, when we created out ``forecaster`` module using the ``startmodule`` command, it generated a file
at ``forecaster/commands.py`` that looks like this:


.. code-block:: python

   import click
   from gluepy.commands import cli


   @cli.command()
   def sample():
       click.echo("Sample command called")


What happens here is the following:

* The command is using `Click <https://click.palletsprojects.com/en/8.1.x/>`_ under the hood for logic related to CLI such as
  adding options, groups of commands, help text and more.
* All commands in Gluepy served on ``manage.py`` is part of the ``gluepy.commands.cli`` group. You must add a command to
  ``gluepy.commands.cli`` using the ``@cli.command()`` operator.

This command can be called using:

.. code-block:: bash

   $ python manage.py sample
   Sample command called


Creating a custom CLI command
=============================

Now let's modify this ``sample`` command to instead receive a path to a run folder, and copy the .pkl model file that we created in :doc:`/intro/tutorial02`
to a ``/data/production`` directory to simulate a deployment. In a real project, you may instead deploy the model to something like `MLFlow <https://mlflow.org/>`_.



.. code-block:: python

   import os
   import click
   from gluepy.commands import cli
   from gluepy.files.storages import default_storage
   from gluepy.conf import default_context


   @cli.command()
   @click.argument("run_folder")
   def deploy(run_folder):
       default_storage.cp(
        os.path.join(run_folder, "model.pkl"),
        os.path.join("production", "model.pkl"),
       )
       click.echo("Model deployed to production")


The code above defines the following:

* Add a new command named ``deploy`` to the ``manage.py`` CLI using the ``@cli.command()`` decorator.
* Add a new argument using `Click <https://click.palletsprojects.com/en/8.1.x/>`_ that expect user to pass a :ref:`context_run_folder` path.
* Use ``default_storage`` to copy the file from our run folder, to a centralized folder we use for "production" models.

This can now be called in the following manner.

.. code-block:: bash

   $ python manage.py deploy runs/2024/6/25/c29b8b49-dee9-4984-8ccc-860651780054/
   Model deployed to production



Wrapping up
===========

That was it for this tutorial. We have now learned:

* How to create new projects
* How to create a :ref:`dags` consisting of 2 :ref:`tasks` that train a machine learning model.
* Using output versioning with :ref:`context_run_folder`. 
* Retrying DAG runs and running subset of runs.
* Parameterizing our model using YAML and :ref:`topic_context`.
* File system interactions with ``default_storage`` and :ref:`topic_storage`.


You should now be familiar with the key concepts of Gluepy. To read more details, see

* :doc:`Topic guides </topics/index>`
* :doc:`Reference guides </ref/index>`
