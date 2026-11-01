# Elasticsearch Comparison Tool

## Project Overview

This project compares two independent Elasticsearch instances
using Python.

## Technologies

- Python
- Elasticsearch 9.5.5
- Docker
- Docker Compose
- VS Code

## Architecture

- Elasticsearch A: localhost:9200
- Elasticsearch B: localhost:9201

## Features

1. Connect to two Elasticsearch instances.
2. Compare index names.
3. Compare document IDs.
4. Detect missing documents.
5. Detect modified documents.
6. Compare individual fields.
7. Generate JSON and CSV reports.

## Installation

Create a virtual environment:

python -m venv venv

Activate:

.\venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

## Run Project

python python/connect.py

python python/create_index.py

python python/insert_data.py

python python/compare_indexes.py

python python/compare_documents.py

python python/main.py