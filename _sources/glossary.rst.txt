========
Glossary
========

.. glossary::

    dag
        A directed-acyclic-graph, or in other words a 'pipeline' of a number of :term:`task` instances
        that are executed in a specific order.

    task
        A single step as part of a :term:`dag`. The task contains the actual logic that is being executed throughout that step.

    schema
        A class that define the structure of your data.

    field
        An attribute on a :term:`schema`; a given field usually maps directly to
        a single dataframe column.

    project
        A Python package -- i.e. a directory of code -- that contains all the
        settings for an instance of Gluepy. This would include data
        configuration, Gluepy-specific options and application-specific
        settings.

    module
        A Python package -- i.e. a directory of code -- that contains a set of DAGs, Commands, Tasks or other
        Gluepy components. Modules can be project specific, or generic and reusable across multiple projects.
