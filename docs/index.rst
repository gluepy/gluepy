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
  :doc:`Part 2: Schemas and data managers <intro/tutorial02>` |
  :doc:`Part 3: Context and configuration parameters <intro/tutorial03>` |
  :doc:`Part 4: Custom CLI commands <intro/tutorial04>`

* **Advanced Tutorials:**
  :doc:`How to write reusable apps <intro/reusable-apps>` |
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

.. * :doc:`How-to guides </howto/index>` are recipes. They guide you through the
..   steps involved in addressing key problems and use-cases. They are more
..   advanced than tutorials and assume some knowledge of how Gluepy works.

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


..   :doc:`Field types <ref/models/fields>` |
..   :doc:`Indexes <ref/models/indexes>` |
..   :doc:`Meta options <ref/models/options>` |
..   :doc:`Model class <ref/models/class>`

.. * **QuerySets:**
..   :doc:`Making queries <topics/db/queries>` |
..   :doc:`QuerySet method reference <ref/models/querysets>` |
..   :doc:`Lookup expressions <ref/models/lookups>`

.. * **Model instances:**
..   :doc:`Instance methods <ref/models/instances>` |
..   :doc:`Accessing related objects <ref/models/relations>`

.. * **Migrations:**
..   :doc:`Introduction to Migrations<topics/migrations>` |
..   :doc:`Operations reference <ref/migration-operations>` |
..   :doc:`SchemaEditor <ref/schema-editor>` |
..   :doc:`Writing migrations <howto/writing-migrations>`

.. * **Advanced:**
..   :doc:`Managers <topics/db/managers>` |
..   :doc:`Raw SQL <topics/db/sql>` |
..   :doc:`Transactions <topics/db/transactions>` |
..   :doc:`Aggregation <topics/db/aggregation>` |
..   :doc:`Search <topics/db/search>` |
..   :doc:`Custom fields <howto/custom-model-fields>` |
..   :doc:`Multiple databases <topics/db/multi-db>` |
..   :doc:`Custom lookups <howto/custom-lookups>` |
..   :doc:`Query Expressions <ref/models/expressions>` |
..   :doc:`Conditional Expressions <ref/models/conditional-expressions>` |
..   :doc:`Database Functions <ref/models/database-functions>`

.. * **Other:**
..   :doc:`Supported databases <ref/databases>` |
..   :doc:`Legacy databases <howto/legacy-databases>` |
..   :doc:`Providing initial data <howto/initial-data>` |
..   :doc:`Optimize database access <topics/db/optimization>` |
..   :doc:`PostgreSQL specific features <ref/contrib/postgres/index>`

.. The view layer
.. ==============

.. Gluepy has the concept of "views" to encapsulate the logic responsible for
.. processing a user's request and for returning the response. Find all you need
.. to know about views via the links below:

.. * **The basics:**
..   :doc:`URLconfs <topics/http/urls>` |
..   :doc:`View functions <topics/http/views>` |
..   :doc:`Shortcuts <topics/http/shortcuts>` |
..   :doc:`Decorators <topics/http/decorators>` |
..   :doc:`Asynchronous Support <topics/async>`

.. * **Reference:**
..   :doc:`Built-in Views <ref/views>` |
..   :doc:`Request/response objects <ref/request-response>` |
..   :doc:`TemplateResponse objects <ref/template-response>`

.. * **File uploads:**
..   :doc:`Overview <topics/http/file-uploads>` |
..   :doc:`File objects <ref/files/file>` |
..   :doc:`Storage API <ref/files/storage>` |
..   :doc:`Managing files <topics/files>` |
..   :doc:`Custom storage <howto/custom-file-storage>`

.. * **Class-based views:**
..   :doc:`Overview <topics/class-based-views/index>` |
..   :doc:`Built-in display views <topics/class-based-views/generic-display>` |
..   :doc:`Built-in editing views <topics/class-based-views/generic-editing>` |
..   :doc:`Using mixins <topics/class-based-views/mixins>` |
..   :doc:`API reference <ref/class-based-views/index>` |
..   :doc:`Flattened index<ref/class-based-views/flattened-index>`

.. * **Advanced:**
..   :doc:`Generating CSV <howto/outputting-csv>` |
..   :doc:`Generating PDF <howto/outputting-pdf>`

.. * **Middleware:**
..   :doc:`Overview <topics/http/middleware>` |
..   :doc:`Built-in middleware classes <ref/middleware>`

.. The template layer
.. ==================

.. The template layer provides a designer-friendly syntax for rendering the
.. information to be presented to the user. Learn how this syntax can be used by
.. designers and how it can be extended by programmers:

.. * **The basics:**
..   :doc:`Overview <topics/templates>`

.. * **For designers:**
..   :doc:`Language overview <ref/templates/language>` |
..   :doc:`Built-in tags and filters <ref/templates/builtins>` |
..   :doc:`Humanization <ref/contrib/humanize>`

.. * **For programmers:**
..   :doc:`Template API <ref/templates/api>` |
..   :doc:`Custom tags and filters <howto/custom-template-tags>` |
..   :doc:`Custom template backend <howto/custom-template-backend>`

.. Forms
.. =====

.. Gluepy provides a rich framework to facilitate the creation of forms and the
.. manipulation of form data.

.. * **The basics:**
..   :doc:`Overview <topics/forms/index>` |
..   :doc:`Form API <ref/forms/api>` |
..   :doc:`Built-in fields <ref/forms/fields>` |
..   :doc:`Built-in widgets <ref/forms/widgets>`

.. * **Advanced:**
..   :doc:`Forms for models <topics/forms/modelforms>` |
..   :doc:`Integrating media <topics/forms/media>` |
..   :doc:`Formsets <topics/forms/formsets>` |
..   :doc:`Customizing validation <ref/forms/validation>`

.. The development process
.. =======================

.. Learn about the various components and tools to help you in the development and
.. testing of Gluepy applications:

.. * **Settings:**
..   :doc:`Overview <topics/settings>` |
..   :doc:`Full list of settings <ref/settings>`

.. * **Applications:**
..   :doc:`Overview <ref/applications>`

.. * **Exceptions:**
..   :doc:`Overview <ref/exceptions>`

.. * **gluepy-admin and manage.py:**
..   :doc:`Overview <ref/gluepy-admin>` |
..   :doc:`Adding custom commands <howto/custom-management-commands>`

.. * **Testing:**
..   :doc:`Introduction <topics/testing/index>` |
..   :doc:`Writing and running tests <topics/testing/overview>` |
..   :doc:`Included testing tools <topics/testing/tools>` |
..   :doc:`Advanced topics <topics/testing/advanced>`

.. * **Deployment:**
..   :doc:`Overview <howto/deployment/index>` |
..   :doc:`WSGI servers <howto/deployment/wsgi/index>` |
..   :doc:`ASGI servers <howto/deployment/asgi/index>` |
..   :doc:`Deploying static files <howto/static-files/deployment>` |
..   :doc:`Tracking code errors by email <howto/error-reporting>` |
..   :doc:`Deployment checklist <howto/deployment/checklist>`

.. The admin
.. =========

.. Find all you need to know about the automated admin interface, one of Gluepy's
.. most popular features:

.. * :doc:`Admin site <ref/contrib/admin/index>`
.. * :doc:`Admin actions <ref/contrib/admin/actions>`
.. * :doc:`Admin documentation generator<ref/contrib/admin/admindocs>`

.. Security
.. ========

.. Security is a topic of paramount importance in the development of web
.. applications and Gluepy provides multiple protection tools and mechanisms:

.. * :doc:`Security overview <topics/security>`
.. * :doc:`Disclosed security issues in Gluepy <releases/security>`
.. * :doc:`Clickjacking protection <ref/clickjacking>`
.. * :doc:`Cross Site Request Forgery protection <ref/csrf>`
.. * :doc:`Cryptographic signing <topics/signing>`
.. * :ref:`Security Middleware <security-middleware>`

.. Internationalization and localization
.. =====================================

.. Gluepy offers a robust internationalization and localization framework to
.. assist you in the development of applications for multiple languages and world
.. regions:

.. * :doc:`Overview <topics/i18n/index>` |
..   :doc:`Internationalization <topics/i18n/translation>` |
..   :ref:`Localization <how-to-create-language-files>` |
..   :doc:`Localized web UI formatting and form input <topics/i18n/formatting>`
.. * :doc:`Time zones </topics/i18n/timezones>`

.. Performance and optimization
.. ============================

.. There are a variety of techniques and tools that can help get your code running
.. more efficiently - faster, and using fewer system resources.

.. * :doc:`Performance and optimization overview <topics/performance>`

.. Geographic framework
.. ====================

.. :doc:`GeoGluepy <ref/contrib/gis/index>` intends to be a world-class geographic
.. web framework. Its goal is to make it as easy as possible to build GIS web
.. applications and harness the power of spatially enabled data.

.. Common web application tools
.. ============================

.. Gluepy offers multiple tools commonly needed in the development of web
.. applications:

.. * **Authentication:**
..   :doc:`Overview <topics/auth/index>` |
..   :doc:`Using the authentication system <topics/auth/default>` |
..   :doc:`Password management <topics/auth/passwords>` |
..   :doc:`Customizing authentication <topics/auth/customizing>` |
..   :doc:`API Reference <ref/contrib/auth>`
.. * :doc:`Caching <topics/cache>`
.. * :doc:`Logging <topics/logging>`
.. * :doc:`Sending emails <topics/email>`
.. * :doc:`Syndication feeds (RSS/Atom) <ref/contrib/syndication>`
.. * :doc:`Pagination <topics/pagination>`
.. * :doc:`Messages framework <ref/contrib/messages>`
.. * :doc:`Serialization <topics/serialization>`
.. * :doc:`Sessions <topics/http/sessions>`
.. * :doc:`Sitemaps <ref/contrib/sitemaps>`
.. * :doc:`Static files management <ref/contrib/staticfiles>`
.. * :doc:`Data validation <ref/validators>`

.. Other core functionalities
.. ==========================

.. Learn about some other core functionalities of the Gluepy framework:

.. * :doc:`Conditional content processing <topics/conditional-view-processing>`
.. * :doc:`Content types and generic relations <ref/contrib/contenttypes>`
.. * :doc:`Flatpages <ref/contrib/flatpages>`
.. * :doc:`Redirects <ref/contrib/redirects>`
.. * :doc:`Signals <topics/signals>`
.. * :doc:`System check framework <topics/checks>`
.. * :doc:`The sites framework <ref/contrib/sites>`
.. * :doc:`Unicode in Gluepy <ref/unicode>`

The Gluepy open-source project
==============================

Learn about the development process for the Gluepy project itself and about how
you can contribute:

* **Community:**
  :doc:`Contributing to Gluepy <internals/contributing/index>` |
  :doc:`Security policies <internals/security>`
..   :doc:`The release process <internals/release-process>` |
..   :doc:`Team organization <internals/organization>` |
..   :doc:`The Gluepy source code repository <internals/git>` |

..   :doc:`Mailing lists and Forum<internals/mailing-lists>`

.. * **Design philosophies:**
..   :doc:`Overview <misc/design-philosophies>`

.. * **Documentation:**
..   :doc:`About this documentation <internals/contributing/writing-documentation>`

.. * **Third-party distributions:**
..   :doc:`Overview <misc/distributions>`

.. * **Gluepy over time:**
..   :doc:`API stability <misc/api-stability>` |
..   :doc:`Release notes and upgrading instructions <releases/index>` |
..   :doc:`Deprecation Timeline <internals/deprecation>`



.. toctree::
    :hidden:
    :maxdepth: 3

    intro/index
    topics/index
    ref/index
    internals/index
    faq/index
    glossary
.. howto/index

.. misc/index
.. releases/index

Indices, glossary and tables
============================

* :ref:`genindex`
* :ref:`modindex`
* :doc:`glossary`