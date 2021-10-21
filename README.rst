Phylm
=====

|PyPI| |Python Version| |License|

|Read the Docs| |Tests| |Codecov|

|pre-commit| |Black|

.. |PyPI| image:: https://img.shields.io/pypi/v/phylm.svg
   :target: https://pypi.org/project/phylm/
   :alt: PyPI
.. |Python Version| image:: https://img.shields.io/pypi/pyversions/phylm
   :target: https://pypi.org/project/phylm
   :alt: Python Version
.. |License| image:: https://img.shields.io/pypi/l/phylm
   :target: https://opensource.org/licenses/MIT
   :alt: License
.. |Read the Docs| image:: https://img.shields.io/readthedocs/phylm/latest.svg?label=Read%20the%20Docs
   :target: https://phylm.readthedocs.io/
   :alt: Read the documentation at https://phylm.readthedocs.io/
.. |Tests| image:: https://github.com/dbatten5/phylm/workflows/Tests/badge.svg
   :target: https://github.com/dbatten5/phylm/actions?workflow=Tests
   :alt: Tests
.. |Codecov| image:: https://codecov.io/gh/dbatten5/phylm/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/dbatten5/phylm
   :alt: Codecov
.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit
.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Black

Film data aggregation.

Motivation
----------

When deciding which film to watch next, it can be helpful to have some key
datapoints at your fingertips, for example, the genre, the cast, the
Metacritic score and, perhaps most importantly, the runtime. This package
provides a `Phylm` class to gather information from various sources for a given
film.


Features
--------

* Get data related to a given film, including runtime, genres, IMDb score and more
* *(coming soon)* Get list of films from a given query title


Installation
------------

You can install *Phylm* via pip_ from PyPI_:

.. code:: console

   $ pip install phylm


Usage
-----

Please see the `Command-line Reference <Usage_>`_ for details.


Contributing
------------

Contributions are very welcome.
To learn more, see the `Contributor Guide`_.


License
-------

Distributed under the terms of the `MIT license`_,
*Phylm* is free and open source software.


Issues
------

If you encounter any problems,
please `file an issue`_ along with a detailed description.


Credits
-------

This project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.

.. _@cjolowicz: https://github.com/cjolowicz
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _MIT license: https://opensource.org/licenses/MIT
.. _PyPI: https://pypi.org/
.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python
.. _file an issue: https://github.com/dbatten5/phylm/issues
.. _pip: https://pip.pypa.io/
.. github-only
.. _Contributor Guide: CONTRIBUTING.rst
.. _Usage: https://phylm.readthedocs.io/en/latest/usage.html
