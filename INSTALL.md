Install virtualenv
```
pyenv virtualenv 3.10.1 cs50
pyenv shell cs50
pyenv local cs50
```

Install requirements
```
poetry lock
poetry install --no-root --no-interaction --no-ansi
```
