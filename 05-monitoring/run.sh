echo "Starting Jupyter Notebook..."
jupyter notebook \
  --ip=0.0.0.0 \
  --port=8001 \
  --no-browser \
  --NotebookApp.token='' \
  --NotebookApp.password='' \
  --allow-root
