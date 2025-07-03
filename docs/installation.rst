.. _installation: 

==================
Installation Guide
==================

MIMIK requires `Python <https://www.python.org/downloads/>`_ 3.9 or newer. 

We use the venv package from the Python standard library to install MIMIK's dependencies without conflicting with existing libraries in your system.

Guide
-----

To check that a compatible version of Python is installed, run:

.. code-block:: bash

    python --version

Run the following commands to clone the MIMIK repository and create and activate a Python virtual environment.

.. code-block:: bash

    git clone git@code.vt.edu:kill-webs/mimik.git
    cd mimik/
    python -m venv venv
    source venv/bin/activate # Linux/macOS
    source venv/Scripts/activate # Windows

Once the environment is activated, run the following commands to install the necessary dependencies.
PyGraphViz requires additional steps that are highlighted below.

.. code-block:: bash

    sudo apt-get install graphviz graphviz-dev
    pip install .


To exit the Python virtual environment, run:

.. code-block:: bash

    deactivate