import json
from pathlib import Path

from connect import get_connections

INDEX_NAME = "employees"

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def load_json(file_name):

    file_path = DATA_DIR / file_name

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def insert_documents(es, records, start_id):

    for position, record in enumerate(records):

        document_id = start_id + position

        es.index(
            index=INDEX_NAME,
            id=document_id,
            document=record
        )

        print(f"Inserted document ID: {document_id}")


def main():

    es_a, es_b = get_connections()

    try:
        employees_a = load_json("employees_a.json")
        employees_b = load_json("employees_b.json")

        print("\nInserting data into Elasticsearch A")

        insert_documents(es_a, employees_a, 101)

        print("\nInserting data into Elasticsearch B")

        insert_documents(es_b, employees_b, 101)

        es_a.indices.refresh(index=INDEX_NAME)
        es_b.indices.refresh(index=INDEX_NAME)

        print("\nEmployee data inserted successfully")

    finally:
        es_a.close()
        es_b.close()


if __name__== "__main__":
    main()