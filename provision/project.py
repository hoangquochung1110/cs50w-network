import os

from invoke import task

from . import common, django


@task
def init(context, clean=False):
    """Prepare env for working with project."""
    common.success("Setting up git config")
    pre_commit(context)
    install_tools(context)
    pip_compile(context)
    django.migrate(context)
    django.createsuperuser(context)


@task
def build(context):
    """Build python environ"""
    install_requirements(context)


@task
def install_tools(context):
    """Install shell/cli dependencies, and tools needed to install requirements

    """
    context.run("pip install --upgrade setuptools pip pip-tools wheel")


@task
def pre_commit(context):
    """Install git hooks via pre-commit."""
    common.success("Setting up pre-commit")
    hooks = " ".join(
        f"--hook-type {hook}" for hook in (
            "pre-commit",
            "pre-push",
            "commit-msg",
        )
    )
    context.run(f"pre-commit install {hooks}")


@task
def install_requirements(context, env="development"):
    """Install local development requirements"""
    common.success("Install requirements with poetry")
    context.run("poetry install --no-root --no-interaction --no-ansi")


@task
def pip_compile(context, update=False):
    """Compile requirements with pip-compile"""
    common.success("Compile requirements with pip-compile")
    upgrade = "-U" if update else ""
    in_files = [
        "requirements/production.in",
        "requirements/development.in",
    ]
    for in_file in in_files:
        context.run(f"pip-compile -q {in_file} {upgrade}")


@task
def init_local_settings(context, force_update=True):
    """Copy local settings from template

    Args:
        force_update(bool): rewrite file if exists or not
    """
    local_settings = "project4/local.py"
    local_template = "project4/local.template.py"

    if force_update or not os.path.isfile(local_settings):
        context.run(" ".join(["cp", local_template, local_settings]))
