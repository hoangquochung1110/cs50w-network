from invoke import Collection

from provision import django, docker, linters, project

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
