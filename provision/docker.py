from invoke import task

from . import common

MAIN_CONTAINERS = [
    "postgres",
    "web",
]


def up_containers(context, containers, detach=True, **kwargs):
    """Bring up containers and run them.

    Add `d` kwarg to run them in background.

    Args:
        context: Invoke context
        containers: Name of containers to start
        detach: To run them in background

    """
    if containers:
        common.success(f"Bring up {', '.join(containers)} containers")
    else:
        common.success("Bring up all containers")
    cmd = (
        f"docker-compose up "
        f"{'-d ' if detach else ''}"
        f"{' '.join(containers)}"
    )
    context.run(cmd)

def stop_containers(context, containers):
    """Stop containers."""
    common.success(f"Stopping {' '.join(containers)} containers ")
    cmd = f"docker-compose stop {' '.join(containers)}"
    context.run(cmd)

@task
def up(context):
    """Bring up main containers and start them."""
    up_containers(
        context,
        containers=MAIN_CONTAINERS,
        detach=True,
    )


@task
def stop(context):
    """Stop main containers."""
    stop_containers(
        context,
        containers=MAIN_CONTAINERS,
    )
