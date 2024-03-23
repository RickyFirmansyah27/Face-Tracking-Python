mkdir -p ~/.streamlit/
echo "\
[server]\n\
headless = true\n\
port = $PORT\n\
enableCORS = false\n\
\n\
" > ~/.streamlit/config.toml

#!/bin/bash


# Install other libraries using pip
pip install -r library.txt

# Run the application
streamlit run streamlit-app.py

