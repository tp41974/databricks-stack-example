# Databricks Stack Example

This example repository demonstrates how to utilize the Databricks CLI
in order to deploy projects across multiple Databricks environments.

To do:

- MVP:
    - [ ] Add multi-task job configuration
    - [ ] Ensure `spark_python_task` tasks accept command line arguments as parameters
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
