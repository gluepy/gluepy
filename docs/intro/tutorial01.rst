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
