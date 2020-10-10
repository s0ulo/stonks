# Stonks

Stonks market analyzer and predictor using Flask, Plotly and [some cool prediction method and modules].

## Documentation

Project description documentation is available [here](https://docs.google.com/document/d/1hyo6X5697rYHlifO1heI5EU1dFaANa5ReJGqzG-3EAg/).

## Requirements

- Python 3.x
- Poetry
- Flask & SQLAlchemy
- plotly
- requests + pandas

### Install [Poetry](https://python-poetry.org/)

Windows powershell:

```console
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
```

macOS / linux / bashonwindows:

```console
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

### Download

**Clone the git repository and install via [Poetry](https://python-poetry.org/)**:

```console
$ git clone https://github.com/s0ulo/stonks.git
$ cd stonks
$ poetry shell
$ poetry update
```

### Run flask app

macOS / linux:

```console
$ export FLASK_APP=stonks_app && export FLASK_ENV=development
$ flask run
```

Windows:

```console
> set FLASK_APP=stonks_app && set FLASK_ENV=development && set FLASK_DEBUG=1

> flask run
```
