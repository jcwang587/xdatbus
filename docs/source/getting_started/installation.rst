Installation
=====

.. _installation:

1. Installing with pip
----------------

Make sure you have a Python interpreter, preferably version 3.10 or higher:

.. code-block:: console

   $ python --version
   Python 3.11.4


To use `xdatbus`, install it from the PyPI repository using ``pip``, which will also ensure that all requirements are obtained in the meantime:

.. code-block:: console

   $ pip install xdatbus

To get the latest version of `xdatbus`, if you have it already installed, please run the command with the ``--upgrade`` option:

.. code-block:: console

   $ pip install --upgrade xdatbus

If you'd like to use the latest unreleased version on the main branch, you can install it directly from `GitHub <https://github.com/jcwang587/xdatbus>`_:

.. code-block:: console

   $ pip install -U git+https://https://github.com/jcwang587/xdatbus


2. Installing with conda
----------------

.. note::

   Conda installation will be made available with an option to install `xdatbus` bundled with `plumed2` in the coming version.

Download and install the version of conda for your operating system from `Miniconda <https://docs.conda.io/projects/miniconda/en/latest/>`_. It is generally recommended you create a separate environment for `xdatbus`. For example:

.. code-block:: console

   $ conda create --name my_xdatbus
   $ conda activate my_xdatbus

You can install `xdatbus` via conda as well via the xdatbus channel on Anaconda cloud:

.. code-block:: console

   $ conda install --channel xdatbus xdatbus


3. Optional installation
----------------

For users who want to use `xdatbus` for 3D visualization, please install the ``opt_bpy`` extra:

.. code-block:: console

   $ pip install xdatbus[opt_bpy]
