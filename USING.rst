Usage
=====


Checking Instance Health
------------------------

You can check the status Dagster instance:

.. code-block:: bash

    dagster_client instance health


Jobs
----

You can see the available jobs:

.. code-block:: bash

    dagster_client jobs list


Runs
----

You can see the list of jobs already run:

.. code-block:: bash

    dagster_client runs list


You can stop a run:

.. code-block:: bash

    dagster_client runs stop <run_id>


You can start a job using a preset:

.. code-block:: bash

    dagster_client runs preset <pipeline_name> <preset_number> [run_config]

Example using preset:

.. code-block:: bash

    dagster_client runs preset my_job 0

Example using customization preset:

.. code-block:: bash

    dagster_client runs preset my_job 0 '{"ops":{"my_ops1":{"config":{"variable":"new_value"}}}}'