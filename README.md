

## Setup

**This project built using Python 3.10.4**

python -m venv venv


pip install -r requirements.txt


docker-compose up --build -d


cd data-import
python create_index.py

python webpages.py
