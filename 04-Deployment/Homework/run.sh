echo "Starting Jupyter Notebook..."
jupyter notebook \
  --ip=0.0.0.0 \
  --port=8000 \
  --no-browser \
  --NotebookApp.token='' \
  --NotebookApp.password='' \
  --allow-root
