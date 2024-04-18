##############################################################################
# System shortcuts
##############################################################################

from invoke import task


def chown(context):
    """Shortcut for owning apps dir by current user after some files were
    generated using docker-compose (migrations, new app, etc)
    """
    context.run("sudo chown ${USER}:${USER} -R apps")


@task
def create_tmp_folder(context):
    """Create folder for temporary files."""
    context.run("mkdir -p .tmp")
