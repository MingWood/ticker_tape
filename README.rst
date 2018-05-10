========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - |
        |
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/ticker_tape/badge/?style=flat
    :target: https://readthedocs.org/projects/ticker_tape
    :alt: Documentation Status

.. |version| image:: https://img.shields.io/pypi/v/ticker-tape.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/ticker-tape

.. |commits-since| image:: https://img.shields.io/github/commits-since/MingWood/ticker_tape/v0.1.0.svg
    :alt: Commits since latest release
    :target: https://github.com/MingWood/ticker_tape/compare/v0.1.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/ticker-tape.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/ticker-tape

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/ticker-tape.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/ticker-tape

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/ticker-tape.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/ticker-tape


.. end-badges

An example package. Generated with cookiecutter-pylibrary.

* Free software: MIT license

Installation
============

::

    pip install ticker-tape

Documentation
=============

https://ticker_tape.readthedocs.io/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
