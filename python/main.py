import json
import csv
from pathlib import Path

from compare_indexes import get_index_names
from compare_documents import get_documents

from connect import get_connections


BASE_DIR = Path(__file__).resolve().parent.parent
REPORT_DIR = BASE_DIR / "reports"

INDEX_NAME = "employees"


def main():

    REPORT_DIR.mkdir(exist_ok=True)

    es_a, es_b = get_connections()

    try:
        # Compare indexes
        indexes_a = get_index_names(es_a)
        indexes_b = get_index_names(es_b)

        # Compare documents
        docs_a = get_documents(es_a)
        docs_b = get_documents(es_b)

        ids_a = set(docs_a)
        ids_b = set(docs_b)

        common_ids = ids_a & ids_b

        matching = []
        modified = []

        for doc_id in sorted(common_ids):

            if docs_a[doc_id] == docs_b[doc_id]:
                matching.append(doc_id)

            else:
                differences = {}

                fields = (
                    set(docs_a[doc_id])
                    | set(docs_b[doc_id])
                )

                for field in fields:

                    value_a = docs_a[doc_id].get(field)
                    value_b = docs_b[doc_id].get(field)

                    if value_a != value_b:
                        differences[field] = {
                            "A": value_a,
                            "B": value_b
                        }

                modified.append({
                    "id": doc_id,
                    "differences": differences
                })

        report = {
            "index_comparison": {
                "common": sorted(indexes_a & indexes_b),
                "only_in_a": sorted(indexes_a - indexes_b),
                "only_in_b": sorted(indexes_b - indexes_a)
            },
            "document_comparison": {
                "total_a": len(docs_a),
                "total_b": len(docs_b),
                "matching": matching,
                "modified": modified,
                "missing_in_a": sorted(ids_b - ids_a),
                "missing_in_b": sorted(ids_a - ids_b)
            }
        }

        # Save JSON report
        json_path = REPORT_DIR / "comparison_report.json"

        with open(json_path, "w", encoding="utf-8") as file:
            json.dump(report, file, indent=4)

        # Save CSV report
        csv_path = REPORT_DIR / "comparison_report.csv"

        with open(csv_path, "w", newline="", encoding="utf-8") as file:

            writer = csv.writer(file)

            writer.writerow([
                "Document ID",
                "Status",
                "Field",
                "Value A",
                "Value B"
            ])

            for doc_id in matching:
                writer.writerow([doc_id, "MATCH", "", "", ""])

            for item in modified:
                for field, values in item["differences"].items():

                    writer.writerow([
                        item["id"],
                        "MODIFIED",
                        field,
                        values["A"],
                        values["B"]
                    ])

            for doc_id in report["document_comparison"]["missing_in_a"]:
                writer.writerow([doc_id, "MISSING_IN_A", "", "", ""])

            for doc_id in report["document_comparison"]["missing_in_b"]:
                writer.writerow([doc_id, "MISSING_IN_B", "", "", ""])

        print("\n========== FINAL COMPARISON ==========")

        print("Documents in A:", len(docs_a))
        print("Documents in B:", len(docs_b))

        print("Matching:", len(matching))
        print("Modified:", len(modified))

        print(
            "Missing in A:",
            len(report["document_comparison"]["missing_in_a"])
        )

        print(
            "Missing in B:",
            len(report["document_comparison"]["missing_in_b"])
        )

        print("\nReports generated successfully!")
        print("JSON:", json_path)
        print("CSV:", csv_path)

    finally:
        es_a.close()
        es_b.close()

if __name__ == "__main__":
    main()