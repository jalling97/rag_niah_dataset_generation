# rag_niah_dataset_generation
Tests and Experiments for generating a needle-in-a-haystack dataset for RAG-focused evaluations

## Install Dependencies
Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate
```

Install the dependencies:
```bash
python -m pip install -r requirements
```

## Usage
The following generation python script uses pandas to create a JSON dataset that injects a secret code hidden in various pieces of text. You can use whatever documentation you like, as long as it is in csv format that contains a `text` field.

```
usage: Needle in a Haystack Dataset Generator [-h] [-f FILES [FILES ...]] [-c COPIES]

Uses a list of documents to generate needle in a haystack tests for RAG evaluations

options:
  -h, --help            show this help message and exit
  -f FILES [FILES ...], --files FILES [FILES ...]
  -c COPIES, --copies COPIES

```

Run the script using the default documents in `paul_graham_essays.csv`

```bash
python niah_generate.py
```