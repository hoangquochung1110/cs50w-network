from invoke import Collection

from provision import ci, django, docker, linters, project

ns = Collection(
    ci,
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
