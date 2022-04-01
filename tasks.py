import json
import os
from pathlib import Path

from databricks_cli.configure.provider import ProfileConfigProvider
from invoke import task
from omegaconf import OmegaConf


BASE_DIR = Path(__file__).resolve().parent
CONF_DIR = BASE_DIR.joinpath("conf")
DIST_DIR = BASE_DIR.joinpath("dist")


def _last_modified_wheel_file() -> Path:
    wheels = DIST_DIR.glob("*.whl")
    wheels_desc = sorted(wheels, key=lambda x: x.stat().st_mtime, reverse=True)
    return wheels_desc[0]

@task
def build(c):
    c.run("python -m build")


@task
def deploy(c, profile, no_build=False, no_overwrite=False):
    """Use the Databricks CLI to deploy project to a databricks environment.

    Args:
        profile (str): The name of the databricks-cli profile to use. This profile
            must be defined in ``~/.databrickscfg``.
        build (bool): Whether to build a new wheel distribution.
        overwrite (bool): Wheteer to overwrite existing files in Databricks.
    """
    if not no_build:
        c.run("python -m build")
    # Get path of latest wheel distribution
    wheel_path = _last_modified_wheel_file()
    # Set wheel path as environment variable to be parsed in stack YAML file
    os.environ["WHEEL_NAME"] = str(wheel_path.name)
    # Load stack YAML and convert to JSON
    stack_yaml_path = CONF_DIR.joinpath("databricks", "stack.yaml")
    stack = OmegaConf.load(stack_yaml_path)
    stack_json_path = CONF_DIR.joinpath("databricks", "stack.json")
    with open(stack_json_path, "w") as f:
        stack_dict = OmegaConf.to_object(stack)
        json.dump(stack_dict, f)

    if not no_overwrite:
        c.run(f'databricks stack --profile {profile} deploy {stack_json_path} --overwrite')
    else:
        c.run(f'databricks stack --profile {profile} deploy {stack_json_path}')
