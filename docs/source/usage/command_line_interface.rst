Command line interface
=====

.. _command-line-interface:

List of recipes
------------

The list of the available `xdatbus` CLI recipes can be displayed by running the ``xdatbus`` command:

.. code-block:: console

   $ xdatbus

Following is the list of available CLI commands:

.. list-table::
   :header-rows: 1

   * - Command
     - Description

   * - ``xdc_aggregate``
     - Aggregate XDATCAR files from an AIMD simulation

   * - ``xdc_unwrap``
     - Unwrap the coordinates in the XDATCAR file (to xyz)

   * - ``thermal_report``
     - Generate a thermal report from the OSZICAR files

   * - ``xml2xyz``
     - Convert the vasprun.xml files to extended xyz files

.. note::

Not all the functionalities are available in the CLI. For the detailed tutorials of the application, please refer to
the `examples <https://github.com/jcwang587/xdatbus/tree/main/examples>`_ directory of the GitHub repository.

Combine trajectories
----------------

Copy the `XDATCAR` files in sequence, naming as `XDATCAR01, XDATCAR02, XDATCAR10` ... or
`XDATCAR1, XDATCAR2, XDATCAR10`...; both formats will work. In the same directory, run the command ``xdc_aggregate``
or use ``xdc_aggregate -h`` for help. The script will first wrap the coordinates within the cell and concatenate
the trajectories using a naming sequence.

.. code-block:: console

   $ xdc_aggregate
    [13:45:19] sequence: ['XDATCAR0', 'XDATCAR1']
    [13:45:22] xdc_aggregate: wrapping XDATCAR0 | number of frames: 2000
    [13:45:25] xdc_aggregate: wrapping XDATCAR1 | number of frames: 2000
    [13:45:30] xdc_aggregate: initializing XDATBUS
    [13:45:36] xdc_aggregate: appending XDATCAR1


Unwrap XDATCAR
----------------

To unwrap the trajectory in the XDATCAR file, run the command ``xdc_unwrap`` or use ``xdc_unwrap -h`` for help.

.. code-block:: console

   $ xdc_unwrap
    [13:50:56] xdc_unwrap: Processing step 100
    [13:50:59] xdc_unwrap: Processing step 200
    [13:51:02] xdc_unwrap: Processing step 300
    [13:51:05] xdc_unwrap: Processing step 400
    [13:51:08] xdc_unwrap: Processing step 500

Generate thermal report
----------------

Copy the OSZICAR files in sequence, naming as `OSZICAR01, OSZICAR02, OSZICAR10` ... or
`OSZICAR1, OSZICAR2, OSZICAR10`...; both formats will work. In the same directory, run the command ``thermal_report``
or use ``thermal_report -h`` for help. The script will export four-column .csv data with `potential energy`,
`kinetic energy`, `total energy`, and `temperature` for each time step.

.. code-block:: console

   $ thermal_report
    [13:59:18] sequence: ['OSZICAR0', 'OSZICAR1']
               thermal_report: Processing OSZICAR0
               thermal_report: Processing OSZICAR1


Convert xml to xyz
----------------

To convert the vasprun.xml files to extended xyz files, run the following command:

.. code-block:: console

   $ xml2xyz

