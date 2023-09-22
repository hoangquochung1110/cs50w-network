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
    common.success(f"Install requirements with pip from {env}.txt")
    context.run(f"pip install -r requirements/{env}.txt")


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
