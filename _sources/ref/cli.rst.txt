============================
Command Line Interface (CLI)
============================

All Gluepy projects have a CLI exposed through the ``manage.py`` file located in project root. This command line interface allow you to
execute your DAGs, retry previous runs and manage your project in various ways.

The CLI comes with a set of commands out of the box, but it is also extendable and allow you to :ref:`cli_custom_commands`.

.. _cli:

Gluepy Commands
===============


.. _cli_dag:

dag command
-----------

This command allow you to run a :ref:`dags` registered in the :ref:`dags_registry` by its ``label`` attribute. The ``label`` attribute
can either be set explicitally, or it default to the lowercase string of the :ref:`dags` class name.

.. autofunction:: gluepy.commands.dag.dag



.. _cli_startproject:

startproject command
--------------------

.. autofunction:: gluepy.commands.gluepy.startproject


.. _cli_startmodule:

startmodule command
-------------------

.. autofunction:: gluepy.commands.gluepy.startmodule


.. _cli_airflow_generate:

airflow generate command
------------------------

This command is used to generate DAG files in Airflow format to be used to run Gluepy DAGs using Airflow as an orchestrator.
The command sits under the ``airflow`` CLI command group and is used by executing ``./manage.py airflow generate``.

The command is leveraging the following settings:

* ``AIRFLOW_TEMPLATE``. Path to ``.j2`` Jinja file that contains template of how the Gluepy DAG is transformed into Airflow format. Defaults to template that generate Airflow DAG using ``KubernetesPodOperator``.
* ``AIRFLOW_DAG_PREFIX``. Prefix in each Airflow DAG file. E.g. your Gluepy DAG is named ``forecaster`` and with ``AIRFLOW_DAG_PREFIX`` set to ``"myproject"`` the resulting Airflow DAGs would be named ``myproject_forecaster``.
* ``AIRFLOW_IMAGE``. Image name to be used in template using the ``KubernetesPodOperator``.
* ``AIRFLOW_CONFIGMAPS``. Configmaps to populate environment variables used in the ``KubernetesPodOperator``.
* ``AIRFLOW_POD_RESOURCES``. Resource limits and requests to be used in the ``KubernetesPodOperator``.
* ``KUBERNETES_CONFIG``. Optional path to the kubernetes config that allow connection to cluster, used in ``KubernetesPodOperator``.


.. autofunction:: gluepy.commands.airflow.generate


.. _cli_custom_commands:

Create your own CLI commands
============================

To write your own custom CLI commands in your project, see our tutorial :doc:`Part 4: Custom CLI commands </intro/tutorial04>`
