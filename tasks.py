from provision import project, linters, docker, django
from invoke import Collection


ns = Collection(
    linters,
    project,
    docker,
    django,
)


# Configurations for run command
ns.configure(
    dict(
        run=dict(
            pty=True,
            echo=True,
        ),
    ),
)
