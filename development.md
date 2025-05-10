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
