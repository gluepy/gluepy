To run the test suite, first, create and activate a virtual environment. Then
install some requirements and run the tests::

    $ cd tests
    $ python -m venv envs/
    $ source envs/bin/activate
    $ python -m pip install -e ..
    $ ./runtests.py
