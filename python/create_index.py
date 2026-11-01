from connect import get_connections

INDEX_NAME = "employees"

# Define the structure of employee documents
MAPPING = {
    "properties": {
        "name": {
            "type": "text"
        },
        "department": {
            "type": "keyword"
        },
        "salary": {
            "type": "integer"
        },
        "location": {
            "type": "keyword"
        }
    }
}


def create_index(es, index_name):

    if es.indices.exists(index=index_name):
        print(f"Index '{index_name}' already exists")
    else:
        es.indices.create(
            index=index_name,
            mappings=MAPPING
        )

        print(f"Index '{index_name}' created successfully")


def main():

    es_a, es_b = get_connections()

    try:
        print("Creating index in Elasticsearch A...")
        create_index(es_a, INDEX_NAME)

        print("\nCreating index in Elasticsearch B...")
        create_index(es_b, INDEX_NAME)

    finally:
        es_a.close()
        es_b.close()


if __name__ == "__main__":
    main()

from connect import get_connections

INDEX_NAME = "employees"

# Define the structure of employee documents
MAPPING = {
    "properties": {
        "name": {
            "type": "text"
        },
        "department": {
            "type": "keyword"
        },
        "salary": {
            "type": "integer"
        },
        "location": {
            "type": "keyword"
        }
    }
}


def create_index(es, index_name):

    if es.indices.exists(index=index_name):
        print(f"Index '{index_name}' already exists")
    else:
        es.indices.create(
            index=index_name,
            mappings=MAPPING
        )

        print(f"Index '{index_name}' created successfully")


def main():

    es_a, es_b = get_connections()

    try:
        print("Creating index in Elasticsearch A...")
        create_index(es_a, INDEX_NAME)

        print("\nCreating index in Elasticsearch B...")
        create_index(es_b, INDEX_NAME)

    finally:
        es_a.close()
        es_b.close()


if __name__ == "__main__":
    main()