|Icon| |title|_
===============

.. |title| replace:: newport-tlb6700
.. _title: https://xkstein.github.io/newport-tlb6700

.. |Icon| image:: https://avatars.githubusercontent.com/xkstein
        :target: https://xkstein.github.io/newport-tlb6700
        :height: 100px

|PyPI| |Forge| |PythonVersion| |PR|

|CI| |Codecov| |Black| |Tracking|

.. |Black| image:: https://img.shields.io/badge/code_style-black-black
        :target: https://github.com/psf/black

.. |CI| image:: https://github.com/xkstein/newport-tlb6700/actions/workflows/matrix-and-codecov-on-merge-to-main.yml/badge.svg
        :target: https://github.com/xkstein/newport-tlb6700/actions/workflows/matrix-and-codecov-on-merge-to-main.yml

.. |Codecov| image:: https://codecov.io/gh/xkstein/newport-tlb6700/branch/main/graph/badge.svg
        :target: https://codecov.io/gh/xkstein/newport-tlb6700

.. |Forge| image:: https://img.shields.io/conda/vn/conda-forge/newport-tlb6700
        :target: https://anaconda.org/conda-forge/newport-tlb6700

.. |PR| image:: https://img.shields.io/badge/PR-Welcome-29ab47ff
        :target: https://github.com/xkstein/newport-tlb6700/pulls

.. |PyPI| image:: https://img.shields.io/pypi/v/newport-tlb6700
        :target: https://pypi.org/project/newport-tlb6700/

.. |PythonVersion| image:: https://img.shields.io/pypi/pyversions/newport-tlb6700
        :target: https://pypi.org/project/newport-tlb6700/

.. |Tracking| image:: https://img.shields.io/badge/issue_tracking-github-blue
        :target: https://github.com/xkstein/newport-tlb6700/issues

Unofficial Newport Velocity TLB6700 tunable laser python driver

* LONGER DESCRIPTION HERE

For more information about the newport-tlb6700 library, please consult our `online documentation <https://xkstein.github.io/newport-tlb6700>`_.

Citation
--------

If you use newport-tlb6700 in a scientific publication, we would like you to cite this package as

        newport-tlb6700 Package, https://github.com/xkstein/newport-tlb6700

Installation
------------

The preferred method is to use `Miniconda Python
<https://docs.conda.io/projects/miniconda/en/latest/miniconda-install.html>`_
and install from the "conda-forge" channel of Conda packages.

To add "conda-forge" to the conda channels, run the following in a terminal. ::

        conda config --add channels conda-forge

We want to install our packages in a suitable conda environment.
The following creates and activates a new environment named ``newport-tlb6700_env`` ::

        conda create -n newport-tlb6700_env newport-tlb6700
        conda activate newport-tlb6700_env

The output should print the latest version displayed on the badges above.

If the above does not work, you can use ``pip`` to download and install the latest release from
`Python Package Index <https://pypi.python.org>`_.
To install using ``pip`` into your ``newport-tlb6700_env`` environment, type ::

        pip install newport-tlb6700

If you prefer to install from sources, after installing the dependencies, obtain the source archive from
`GitHub <https://github.com/xkstein/newport-tlb6700/>`_. Once installed, ``cd`` into your ``newport-tlb6700`` directory
and run the following ::

        pip install .

This package also provides command-line utilities. To check the software has been installed correctly, type ::

        newport-tlb6700 --version

You can also type the following command to verify the installation. ::

        python -c "import newport_tlb6700; print(newport_tlb6700.__version__)"


To view the basic usage and available commands, type ::

        newport-tlb6700 -h

Getting Started
---------------

You may consult our `online documentation <https://xkstein.github.io/newport-tlb6700>`_ for tutorials and API references.

Support and Contribute
----------------------

If you see a bug or want to request a feature, please `report it as an issue <https://github.com/xkstein/newport-tlb6700/issues>`_ and/or `submit a fix as a PR <https://github.com/xkstein/newport-tlb6700/pulls>`_.

Feel free to fork the project and contribute. To install newport-tlb6700
in a development mode, with its sources being directly used by Python
rather than copied to a package directory, use the following in the root
directory ::

        pip install -e .

To ensure code quality and to prevent accidental commits into the default branch, please set up the use of our pre-commit
hooks.

1. Install pre-commit in your working environment by running ``conda install pre-commit``.

2. Initialize pre-commit (one time only) ``pre-commit install``.

Thereafter your code will be linted by black and isort and checked against flake8 before you can commit.
If it fails by black or isort, just rerun and it should pass (black and isort will modify the files so should
pass after they are modified). If the flake8 test fails please see the error messages and fix them manually before
trying to commit again.

Improvements and fixes are always appreciated.

Before contributing, please read our `Code of Conduct <https://github.com/xkstein/newport-tlb6700/blob/main/CODE-OF-CONDUCT.rst>`_.

Contact
-------

For more information on newport-tlb6700 please visit the project `web-page <https://xkstein.github.io/>`_ or email Jamie at jamie.k.eckstein@gmail.com.

Acknowledgements
----------------

``newport-tlb6700`` is built and maintained with `scikit-package <https://scikit-package.github.io/scikit-package/>`_.
