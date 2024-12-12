====================
Gluepy documentation
====================

.. rubric:: Everything you need to know about Gluepy.

.. _index-first-steps:

First steps
===========

Are you new to Gluepy or to programming? This is the place to start!

* **From scratch:**
  :doc:`Overview <intro/overview>` |
  :doc:`Installation <intro/install>`

* **Tutorial:**
  :doc:`Part 1: DAGs and Tasks <intro/tutorial01>` |
  :doc:`Part 2: Data managers <intro/tutorial02>` |
  :doc:`Part 3: Context and configuration parameters <intro/tutorial03>` |
  :doc:`Part 4: Custom CLI commands <intro/tutorial04>`

* **Advanced Tutorials:**
  :doc:`Writing your first patch for Gluepy <intro/contributing>`

Getting help
============

Having trouble? We'd like to help!

* Try the :doc:`FAQ <faq/index>` -- it's got answers to many common questions.

* Looking for specific information? Try the :ref:`genindex`, :ref:`modindex` or
  the :doc:`detailed table of contents <contents>`.

* Not found anything? See :doc:`faq/help` for information on getting support
  and asking questions to the community.

* Report bugs with Gluepy in our `ticket tracker`_.

.. _ticket tracker: https://github.com/gluepy/gluepy/issues

How the documentation is organized
==================================

Gluepy has a lot of documentation. A high-level overview of how it's organized
will help you know where to look for certain things:

* :doc:`Tutorials </intro/index>` take you by the hand through a series of
  steps to create a web application. Start here if you're new to Gluepy or web
  application development. Also look at the ":ref:`index-first-steps`".

* :doc:`Topic guides </topics/index>` discuss key topics and concepts at a
  fairly high level and provide useful background information and explanation.

* :doc:`Reference guides </ref/index>` contain technical reference for APIs and
  other aspects of Gluepy's machinery. They describe how it works and how to
  use it but assume that you have a basic understanding of key concepts.


Execution Layer
===============

Gluepy provides multiple tools and abstractions related to "Executing" your Machine Learning
or Data pipelines both from how to structure the execution, to triggering the execution itself.
Learn more about it below:

* **DAG:**
  :doc:`Introduction to DAGs </topics/dags>` |
  :doc:`DAG reference </ref/dags>` |
  :ref:`Task reference <tasks>`

* **Commands:**
  :doc:`Introduction to CLI </ref/cli>` |
  :ref:`cli_dag` |
  :ref:`cli_startproject` |
  :ref:`cli_startmodule` |
  :ref:`cli_airflow_generate`


File Layer
==========

Data and file interactions is a primary citizen of the Gluepy framework, and it provides a set of
utilities, abstractions and useful tools to interact with the file system and read data.

* **Storages:**
  :ref:`Introduction to Storage <topic_storage>` |
  :ref:`storage_backend_base` |
  :ref:`storage_backend_local` |
  :ref:`storage_backend_google` |
  :ref:`storage_backend_s3`

* **Data Managers:**
  :ref:`Introduction to Data Managers <topic_data>` |
  :ref:`data_backends` |
  :ref:`data_backend_pandas` |
  :ref:`data_backend_base`


The development process
=======================

Learn about the various components and tools to help you in the development and
testing of Gluepy applications:

* **Settings:**
  :doc:`Overview <topics/configuration>` |
  :doc:`Full list of settings <ref/settings>`

Security
========

Security is a topic of paramount importance in the development of web
applications and Gluepy provides multiple protection tools and mechanisms:

* :doc:`Security overview <internals/security>`

The Gluepy open-source project
==============================

Learn about the development process for the Gluepy project itself and about how
you can contribute:

* **Community:**
  :doc:`Contributing to Gluepy <internals/contributing/index>` |
  :doc:`Security policies <internals/security>`


.. toctree::
    :hidden:
    :maxdepth: 3

    intro/index
    topics/index
    ref/index
    internals/index
    faq/index
    glossary
    acknowledgements

Indices, glossary and tables
============================

* :ref:`genindex`
* :ref:`modindex`
* :doc:`contents`
* :doc:`glossary`
