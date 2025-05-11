#!/bin/bash
jupyter notebook \
  --ip=0.0.0.0 \
  --port=8000 \
  --allow-root \
  --no-browser \
  --NotebookApp.token='' \
  --NotebookApp.password=''