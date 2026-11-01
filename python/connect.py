from elasticsearch import Elasticsearch

# Elasticsearch server URLs
ES_A_URL = "http://localhost:9200"
ES_B_URL = "http://localhost:9201"


def get_connections():

    es_a = Elasticsearch(ES_A_URL)
    es_b = Elasticsearch(ES_B_URL)

    return es_a, es_b


def test_connections():

    es_a, es_b = get_connections()

    try:
        print("Checking Elasticsearch A...")

        if es_a.ping():
            print("Elasticsearch A connected successfully")
        else:
            print("Elasticsearch A connection failed")

        print("\nChecking Elasticsearch B...")

        if es_b.ping():
            print("Elasticsearch B connected successfully")
        else:
            print("Elasticsearch B connection failed")

    finally:
        es_a.close()
        es_b.close()


if __name__ == "__main__":
    test_connections()