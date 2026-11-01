from connect import get_connections


def get_index_names(es):

    indexes = es.indices.get(index="*")

    return set(indexes.keys())


def compare_indexes():

    es_a, es_b = get_connections()

    try:
        indexes_a = get_index_names(es_a)
        indexes_b = get_index_names(es_b)

        common = indexes_a & indexes_b
        only_a = indexes_a - indexes_b
        only_b = indexes_b - indexes_a

        print("\n========== INDEX COMPARISON ==========")

        print("\nCommon indexes:")
        for index in sorted(common):
            print(index)

        print("\nIndexes only in A:")
        for index in sorted(only_a):
            print(index)

        print("\nIndexes only in B:")
        for index in sorted(only_b):
            print(index)

    finally:
        es_a.close()
        es_b.close()


if __name__ == "__main__":
    compare_indexes()