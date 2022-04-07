# Databricks Stack Example

This example repository demonstrates how the Databricks CLI can be used
to deploy projects across multiple Databricks environments.

To do:

- MVP:
    - [X] Add multi-task job configuration
    - [X] Ensure `spark_python_task` tasks accept command line arguments as parameters
- Enhancements:
    - [ ] Use git filesystem to automate workspace/dbfs configuration
    - [ ] Explore environment variables vs parameters for tasks


## Installation

Clone this repository

```sh
git clone git@github.com:tp41974/databricks-stack-example.git
```

Change directory into the cloned repository

```sh
cd databricks-stack-example
```

Install the required packages

```sh
pip install -r requirements.txt
```

Install the `databricks_stack_example` package locally

```sh
pip install -e .
```

## Directory structure

```
|-- conf <- The top-level configuration directory
    |-- databricks
        |-- stack.yaml        <- Editable configuration file for databricks-cli stack command.
        |-- stack.json        <- Generated configuration file for databricks-cli stack command (excluded from source control).
        |-- stack.deployed.json        <- Stack state file produced by databricks-cli stack command.
|-- data        <- The top-level data directory
|-- databricks_stack_example        <- The Python package.
    |-- __init__.py
    |-- scripts        <- Python scripts that accept command-line arguments. These represent individual tasks to be executed by a job.
        |-- task1.py
        |-- task2.py
        |-- task3.py
|-- dist        <- Built Python distribution files
|-- notebooks        <- Jupyter notebooks
tasks.py        <- management commands like `build` and `deploy`
```

## Usage

> Warning: The environment variables defined in [.env.example](./.env.example)
> must be available before referencing them in the stack configuration file
> or before executing any management commands.

### Define resources

The databricks CLI can be used to deploy a "stack" of resources to Databricks.

A stack consists of three types of resources:

1. Workspace resouces (notebooks)
2. DBFS resources (arbitrary files)
3. Jobs resources

The way you define each resource you want deployed changes based on the type
of resource it is. In general though each resource has the attributes:

- A unique identifier
- The resource type
- The local path of the resource
- The deployed path of the resource on Databricks
- Additional configuration options

You define your stack in a
[stack configuration YAML file](./conf/databricks/stack.yaml).
This file follows a specific
[schema](https://docs.microsoft.com/en-us/azure/databricks/dev-tools/cli/stack-cli#--stack-configuration-template-schema)
defined by Databricks.

The stack configuration YAML file is processed using the
[`omegaconf`](https://omegaconf.readthedocs.io/en/2.1_branch/index.html#) library.
This allows you to reference environment variables within the YAML file using
the `oc.env` [built-in resolver](https://omegaconf.readthedocs.io/en/2.1_branch/usage.html#built-in-resolvers).

### Deploy resources

[tasks.py](./tasks.py) includes two management commands that can be used to
build and deploy your project.

`invoke build` will build a wheel distribution for your Python package and
save it to the `dist/` directory.

`invoke deploy` will build your package (optional) and then deploy resources
to a Databricks environment. The resources that you want to deploy must be
defined in [stack.yaml](./conf/databricks/stack.yaml). This command expects a
`profile` argument which corresponds to the
[Databricks CLI profile](https://docs.microsoft.com/en-us/azure/databricks/dev-tools/cli/#--set-up-authentication) you want to use for authentication.
This profile also determines which environment the resources get deployed to.
For example, if you wanted to deploy your project to the development
Databricks environment, you would run ```sh invoke deploy development```.
This command would fail if you do not have a "development" profile configured
in `.databrickscfg`. This command also accepts two additional options:

- --no-build: Pass this option if you want to skip building a distribution for your Python package.
- --no-overwrite: Pass this option if you do not want to overwrite existing remote resources.

Once the resources are deployed, a stack status JSON file is saved in the same
directory as the stack configuration file.