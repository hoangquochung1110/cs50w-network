from . import docker

WAIT_FOR_IT_FILE = "provision/wait-for-it.sh"
WAIT_FOR_IT_SCRIPT = f"./{WAIT_FOR_IT_FILE} postgres:5432 -- "

def run_local_python(context, command: str, watchers=()):
    """Run command using local python interpreter."""
    docker.up(context)
    return context.run(
        " ".join(["python3", command]),
        watchers=watchers,
    )
