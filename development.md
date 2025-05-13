# Development

Development is on the `develop` branch. Please send PR there.

This project is set up to use uv to manage Python and
dependencies. First, install [uv](https://github.com/astral-sh/uv).


A [`Makefile`](Makefile) simply offers shortcuts to `uv` commands for developer convenience.

```sh
# Install all dependencies and set up your virtual environment.
make install

# Run uv sync, lint, and test:
make

# Build wheel:
make build

# Linting:
make lint

# Run tests:
make test

# Delete all the build artifacts:
make clean

# Upgrade dependencies to compatible versions:
make upgrade
```

To test with a specific version of Python, use the [`UV_PYTHON`](https://docs.astral.sh/uv/configuration/environment/#uv_python) environment variable. For example,

```sh
UV_PYTHON=3.8 make
```

will install and use Python 3.8.
