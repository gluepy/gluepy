======================
Contributing to Gluepy
======================

As a open source framework, you are very welcome to be part of the Gluepy contributing team
by writing your own patch to the Gluepy framework. The patch can range from improvements to the code,
better documentation or new features.

To know what features to work on, please review our `issue tracker <https://github.com/gluepy/gluepy/issues>`_
and look for any issue that has been tagged as ``approved``. These issues has been aligned, discussed and
approved by the Gluepy core team as something that we collectively agreed to make
part of the Framework.


Design Philosophy
=================

Gluepy is attempting to be a simple Framework that is agnostic to use case and most technology choices.
Here are some key points that guide our decision making:

* Gluepy is not limited to a specific cloud provider.
* Gluepy is not limited to a single Dataframe library.
* Gluepy should be modular and allow users to replace built in components
  with their own alternative, e.g. switch out ``LocalStorage`` to a ``UserCustomStorage``.
* Gluepy should be agnostic to use case. We do not concern ourselves with if the user
  is writing Neural Networks, Regression models, Classification models or Data Transformations.
* Gluepy primary purpose is to provide an opinionated structure that guide less technical
  Data Scientist into adhering to best practices without them having to make that a concious decision.


Write your own patch
====================

As mentioned above, you can find issues to work on in our `issue tracker <https://github.com/gluepy/gluepy/issues>`_. Please
only work on issues tagged as ``approved``. If you want to work on an issue that is not approved or listed in the issue tracker,
please consider :ref:`contribute_custom_library`.

The completed issue should be written on a ``feature/``, ``bugfix/`` or ``docs/`` branch, and then be shared as a Pull Request
for further review.

Before review, the pull request is expected to contain:

* A very clear description of the purpose of the pull request, and which issue in the `issue tracker <https://github.com/gluepy/gluepy/issues>`_ it is resolving.
* Lint / Static Analysis complete and passing.
* Unit tests passing.


.. _contribute_custom_library:

Creating a standalone Gluepy library
------------------------------------

You may have an excellent idea that isn't on the roadmap of our `issue tracker <https://github.com/gluepy/gluepy/issues>`_ but
still something that you feel passionate about. It may be a niche use case, or something that you simply want to be owning the
contributions of in the future.

In these situations, feel free to create your own custom Gluepy Module. Please see
:ref:`topic_modules` of how you can write a custom module that other users can enable
in their own Gluepy projects.



Running Lint and Style Checks
=============================

The Gluepy repository comes bundled with a ``.pre-commit-config.yaml`` file that
defines a list of static code analysis checks to execute before a commit.

These checks ensures there are no secrets stored in the code, that the code adhere to formatting
and style rules, and auto format your code using Black.

To run the pre-commit hooks to ensure your code is valid, simply run the following command:

.. code-block:: bash

   $ pre-commit run -a


Running Test Suite
==================

To run the test suite, first, create and activate a virtual environment. Then
install some requirements and run the tests::



    $ cd tests
    $ python -m venv envs/
    $ source envs/bin/activate
    $ python -m pip install -e ..
    $ ./runtests.py
