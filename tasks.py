from provision import project, linters
from invoke import Collection


ns = Collection(
    linters,
    project,
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
