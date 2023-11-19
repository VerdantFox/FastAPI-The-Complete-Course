#!/usr/bin/env bash

run_python_module() {
  # Accept a path as an argument
  path=$1

  # Remove the leading './' from the path if it exists
  path=${path#./}

  # Replace all '/' with '.'
  path=${path//\//.}

  # Remove the file extension
  path=${path%.*}

  eval "python -m $path"
}

run_python_module $1
