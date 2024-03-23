#!/bin/bash

# Create Streamlit configuration if not already present
mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
" > ~/.streamlit/config.toml

# Install OpenCV using Conda
conda activate base
conda install -y -c conda-forge opencv

# Install other libraries using pip
pip install -r library.txt

# Run the Streamlit application
streamlit run streamlit-app.py
