===================
Quick install guide
===================

Before you can use Gluepy, you'll need to get it installed. This guide will guide you to a minimal
installation that'll work while you walk through the introduction.

Install Python
==============

Being a Python web framework, Gluepy requires Python. See
:ref:`faq-python-version-support` for details.

Get the latest version of Python at https://www.python.org/downloads/ or with
your operating system's package manager.

You can verify that Python is installed by typing ``python`` from your shell;
you should see something like:

.. code-block:: pycon

    Python 3.x.y
    [GCC 4.x] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>>

Install Gluepy
==============


Verifying
=========

To verify that Gluepy can be seen by Python, type ``python`` from your shell.
Then at the Python prompt, try to import Gluepy:

.. parsed-literal::

    >>> import gluepy
    >>> print(gluepy.VERSION)
    |version|

You may have another version of Gluepy installed.

That's it!
==========

That's it -- you can now :doc:`move onto the tutorial </intro/tutorial01>`.
