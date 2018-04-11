MultiPath
=========

A miniscule python package for joining and resolving paths against
multiple possible directories.

[`documentation <https://adamkewley.github.io/multipath/>`_]


Installation
------------

To install use pip:

    $ pip install multipath


Or clone the repo:

    $ git clone https://github.com/adamkewley/multipath.git
    $ python setup.py install


Example Usage
-------------

.. code:: python

    import multipath

    paths = [
        "./",
        "~/.someapp/",
        "etc/someapp/",
    ]

    # returns:
    #   './config.yml` if it exists; or,
    #   '~/.someapp/config.yml` if it exists; or,
    #   'etc/someapp/config.yml` if it exists; or,
    #   raises FileNotFoundError
    config = multipath.resolve(paths, "config.yml")
