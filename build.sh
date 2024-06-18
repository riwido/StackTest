#!/usr/bin/env bash

set -e

npm run build
python -m build
