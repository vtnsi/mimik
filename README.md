# MIMIK

Version 1.0

![MIMIK Logo](resources/logo.png)

Read full documentation [here](https://vtnsi.github.io/mimik/index.html "Documentation at vtnsi.github.io")

-----

## Publications

Software Associated with the following publication [Probabilistic Models for Military Kill Chains](https://www.mdpi.com/2079-8954/13/10/924)

## Table of Contents

- [Installation](#installation)
- [License](#license)

## Installation

Requires:
    C/C++ compiler
    [Graphviz](https://www.graphviz.org/)

```
$ python -m venv venv
```

Linux/macOS:

```
$ source ./venv/bin/activate
$ sudo apt-get install graphviz graphviz-dev
$ pip install .
```

Windows:

Install [GraphViz]([Graphviz](https://www.graphviz.org/))

```
$ source ./venv/Scripts/activate
$ pip install -r requirements.txt
$ pip install --config-settings="--global-option=build_ext" --config-settings="--global-option=-IC:\Program Files\Graphviz\include"       --config-settings="--global-option=-LC:\Program Files\Graphviz\lib" pygraphviz
$ pip install .
```

## Utilizing the Examples

Included within this repository is an example used to show our finidings when it comes to modelling, visualizing, and analyzing killwebs.
This notebook can be run after the installation has occurred. The first example can be found within the "1_long_range_strikes_example" directory, and the notebook will provide all the information you will need to run and understand the code.

## Creating Your Own Example

To create your own example for modelling killwebs, you will 3 things of your own:
1. A configs directory containing JSON files which hold the killweb data including all systems, components, and the connections between in addtion to all labels and parameters used for calculations.

2. A tasks directory which contains individual class files. These class files should each hold an init function and a forward function used to calculate the probability given a series of attributes. The example provided includes 4 classes for the F2T2EA mission engineering framework, but other frameworks can be supplemented instead so long as it is consistent with your config files.

3. Finally, you will need to create a notebook with a similar structure to the example notebook. This includes a custom component class, loading the data, and calling all killweb, component graph, or system graph functions you would like to use.

## Config File Creation

To ensure that all config files are compatible with our systems, a JSON schema was created to validate input configs.

To begin, an object should be created with the key equal to the name of your killweb.
The killweb object should contain a series of comma separated child objects

* Each of these systems is a child object with a property being the component name.
    * A component object has 2 properties in "attributes" and "connected_components"
        * The value of "attributes" should be an object in which 3 keys are used. Each of these keys are optional, but some MIMIK functionality might require these fields to be present.
            * "task" should have a value equal to the name of the task associated with the component
            * "task_arguments" has a non specific object containing a series of key value pairs for input parameters
            * "system_name" has a value equal to the name of the parent system containing the component
            * "connected_components" is an array containing the names of each component the current points to
            * NOTE: This component should only point to components associated with the next task
        * "connected_component" is an array of string that includes the name of each component that the current component points to.

## Authors

* [Stephen Adams](https://nationalsecurity.vt.edu/personnel-directory/adams-stephen.html)
* [Michael "Alex" Kyer](https://nationalsecurity.vt.edu/personnel-directory/kyer-alex.html)
* [Dan Sobien](https://nationalsecurity.vt.edu/personnel-directory/sobien-daniel.html)
* [Brian Lee](https://nationalsecurity.vt.edu/personnel-directory/lee-brian.html)

## License

`mimik` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
