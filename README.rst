========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - tests
      - | |travis| |appveyor| |requires|
        | |coveralls| |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |travis| image:: https://api.travis-ci.org/erpbrasil/erpbrasil.edoc.pdf.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/erpbrasil/erpbrasil.edoc.pdf

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/erpbrasil/erpbrasil.edoc.pdf?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/erpbrasil/erpbrasil.edoc.pdf

.. |requires| image:: https://requires.io/github/erpbrasil/erpbrasil.edoc.pdf/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/erpbrasil/erpbrasil.edoc.pdf/requirements/?branch=master

.. |coveralls| image:: https://coveralls.io/repos/erpbrasil/erpbrasil.edoc.pdf/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/erpbrasil/erpbrasil.edoc.pdf

.. |codecov| image:: https://codecov.io/github/erpbrasil/erpbrasil.edoc.pdf/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/erpbrasil/erpbrasil.edoc.pdf

.. |version| image:: https://img.shields.io/pypi/v/erpbrasil.edoc.pdf.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/erpbrasil.edoc.pdf

.. |wheel| image:: https://img.shields.io/pypi/wheel/erpbrasil.edoc.pdf.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/erpbrasil.edoc.pdf

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/erpbrasil.edoc.pdf.svg
    :alt: Supported versions
    :target: https://pypi.org/project/erpbrasil.edoc.pdf

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/erpbrasil.edoc.pdf.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/erpbrasil.edoc.pdf

.. |commits-since| image:: https://img.shields.io/github/commits-since/erpbrasil/erpbrasil.edoc.pdf/v0.2.0.svg
    :alt: Commits since latest release
    :target: https://github.com/erpbrasil/erpbrasil.edoc.pdf/compare/v0.2.0...master



.. end-badges

Impressão de documentos fiscais a partir do XML: NF-E, NFC-E, CT-E, MDF-E, GNRE e etc.

* Free software: MIT license

Installation
============

::

    pip install erpbrasil.edoc.pdf

You can also install the in-development version with::

    pip install https://github.com/erpbrasil/erpbrasil.edoc.pdf/archive/master.zip


Documentation
=============

https://erpbrasil.github.io/docs/

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
