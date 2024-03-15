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


Aggregate XDATCAR
----------------

To aggregate the XDATCAR files from an AIMD simulation, run the following command:

.. code-block:: console

   $ aggregate_xdatcar

Unwrap XDATCAR
----------------

To unwrap the coordinates in the XDATCAR file, run the following command:

.. code-block:: console

   $ xdc_unwrap

Generate thermal report
----------------

To generate a thermal report from the OSZICAR files, run the following command:

.. code-block:: console

   $ thermal_report


Convert xml to xyz
----------------

To convert the vasprun.xml files to extended xyz files, run the following command:

.. code-block:: console

   $ xml2xyz

