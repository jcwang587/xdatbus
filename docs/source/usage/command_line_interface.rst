Command line interface
=====

.. _command-line-interface:

1. List of Recipes
------------

The list of the available `xdatbus` CLI recipes can be displayed by running the ``xdatbus`` command:

.. code-block:: console

   $ xdatbus

Following is the list of available CLI commands:

.. list-table:: XDATBUS CLI recipes
   :header-rows: 1

   * - Command
     - Options
     - Description

   * - ``xdc_aggregate``
     - [--xdc_dir] [--output_dir] [--del_temp]
     - Aggregate XDATCAR files from an AIMD simulation

   * - ``xdc_unwrap``
     - [--xdc_path] [--output_path]
     - Unwrap the coordinates in the XDATCAR file (to xyz)

2. Creating recipes
----------------

To retrieve a list of random ingredients,
you can use the ``lumache.get_random_ingredients()`` function:

.. autofunction:: lumache.get_random_ingredients

The ``kind`` parameter should be either ``"meat"``, ``"fish"``,
or ``"veggies"``. Otherwise, :py:func:`lumache.get_random_ingredients`
will raise an exception.

.. autoexception:: lumache.InvalidKindError

For example:

>>> import lumache
>>> lumache.get_random_ingredients()
['shells', 'gorgonzola', 'parsley']

