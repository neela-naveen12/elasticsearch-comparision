from connect import get_connections
from elasticsearch.helpers import scan

INDEX_NAME = "employees"


def get_documents(es):

    documents = {}

    results = scan(
        es,
        index=INDEX_NAME,
        query={"query": {"match_all": {}}}
    )

    for item in results:

        document_id = item["_id"]
        source = item["_source"]

        documents[document_id] = source

    return documents


def compare_documents():

    es_a, es_b = get_connections()

    try:
        docs_a = get_documents(es_a)
        docs_b = get_documents(es_b)

        ids_a = set(docs_a.keys())
        ids_b = set(docs_b.keys())

        common_ids = ids_a & ids_b

        missing_in_a = ids_b - ids_a
        missing_in_b = ids_a - ids_b

        matching = []
        modified = []

        print("\n========== DOCUMENT COMPARISON ==========")

        for document_id in sorted(common_ids):

            if docs_a[document_id] == docs_b[document_id]:

                matching.append(document_id)

            else:

                differences = {}

                all_fields = (
                    set(docs_a[document_id].keys())
                    | set(docs_b[document_id].keys())
                )

                for field in all_fields:

                    value_a = docs_a[document_id].get(field)
                    value_b = docs_b[document_id].get(field)

                    if value_a != value_b:

                        differences[field] = {
                            "A": value_a,
                            "B": value_b
                        }

                modified.append({
                    "id": document_id,
                    "differences": differences
                })

        print("\nMatching documents:", matching)
        print("Modified documents:", modified)
        print("Missing in A:", sorted(missing_in_a))
        print("Missing in B:", sorted(missing_in_b))

        return {
            "matching": matching,
            "modified": modified,
            "missing_in_a": sorted(missing_in_a),
            "missing_in_b": sorted(missing_in_b)
        }

    finally:
        es_a.close()
        es_b.close()


if __name__ == "_main_":
    compare_documents()