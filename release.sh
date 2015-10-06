#!/usr/bin/env bash

# PyPI configuration file for twine
cat > ~/.pypirc <<- EndOfMessage
[pypi]
repository: https://${PYPI_SERVER}.python.org/pypi
username: ${PYPI_USER}
password: ${PYPI_PASS}
EndOfMessage

tox -e py27,release-nix
tox -e py34,release-nix
