#!/usr/bin/env bash
# enter script dir
cd "$( dirname -- "$BASH_SOURCE"; )";
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
