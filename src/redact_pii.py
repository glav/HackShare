import csv
import pprint
import argparse
import os
from typing import List, Iterable, Optional

from presidio_analyzer import BatchAnalyzerEngine, DictAnalyzerResult
from presidio_anonymizer import BatchAnonymizerEngine

"""
Example implementing a CSV analyzer

This example shows how to use the Presidio Analyzer and Anonymizer
to detect and anonymize PII in a CSV file.
It uses the BatchAnalyzerEngine to analyze the CSV file, and
BatchAnonymizerEngine to anonymize the requested columns.

Usage Instructions:

This script detects and anonymizes PII (Personally Identifiable Information) in CSV files.

Basic usage:
    python src/redact_pii.py

Options:
    --csv-file      Path to the CSV file to analyze (default: './data/support_queries.csv')
    --output-file   Path for the anonymized output CSV file (default: input filename with "-anonymized" suffix)
    --language      Language for PII detection (default: 'en')
    --exclude-columns  List of column names to exclude from redaction
    --threshold     Confidence threshold for detection (default: 0.4, lower is more sensitive)

Examples:
    # Process the default CSV file
    python src/redact_pii.py

    # Process a specific CSV file
    python src/redact_pii.py --csv-file ./path/to/your/file.csv

    # Specify an output file
    python src/redact_pii.py --output-file ./path/to/output.csv

    # Exclude specific columns from redaction
    python src/redact_pii.py --exclude-columns id city

    # Use a more sensitive threshold for detection
    python src/redact_pii.py --threshold 0.3

    # Process a specific file with a specific language and exclude columns
    python src/redact_pii.py --csv-file ./data/custom.csv --language es --exclude-columns id timestamp
"""


class CSVAnalyzer(BatchAnalyzerEngine):

    def analyze_csv(
        self,
        csv_full_path: str,
        language: str,
        keys_to_skip: Optional[List[str]] = None,
        **kwargs,
    ) -> Iterable[DictAnalyzerResult]:

        with open(csv_full_path, 'r') as csv_file:
            csv_list = list(csv.reader(csv_file))
            csv_dict = {header: list(map(str, values)) for header, *values in zip(*csv_list)}
            analyzer_results = self.analyze_dict(csv_dict, language, keys_to_skip, **kwargs)
            return list(analyzer_results)


def write_dict_to_csv(data_dict: dict, output_path: str) -> None:
    """
    Write dictionary data to a CSV file.

    Args:
        data_dict: Dictionary with column names as keys and lists as values
        output_path: Path to write the CSV file
    """
    # Ensure output directory exists
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    headers = list(data_dict.keys())
    max_rows = max(len(values) for values in data_dict.values())

    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write headers
        writer.writerow(headers)
        # Write data rows
        for i in range(max_rows):
            row = [data_dict[header][i] if i < len(data_dict[header]) else '' for header in headers]
            writer.writerow(row)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Redact PII from CSV files")
    parser.add_argument(
        "--csv-file",
        type=str,
        default="./data/support_queries.csv",
        help="Path to the CSV file to analyze"
    )
    parser.add_argument(
        "--output-file",
        type=str,
        default=None,
        help="Path for the anonymized output CSV file"
    )
    parser.add_argument(
        "--language",
        type=str,
        default="en",
        help="Language for PII detection"
    )
    parser.add_argument(
        "--exclude-columns",
        type=str,
        nargs="+",
        default=None,
        help="List of column names to exclude from redaction"
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.4,
        help="Confidence threshold for detection (0.0-1.0, lower is more sensitive)"
    )
    args = parser.parse_args()

    # Set default output file if not provided
    if not args.output_file:
        base, ext = os.path.splitext(args.csv_file)
        args.output_file = f"{base}-anonymized{ext}"

    print(f"Processing file: {args.csv_file}")
    print(f"Output file: {args.output_file}")
    print(f"Language: {args.language}")
    print(f"Excluding columns: {args.exclude_columns if args.exclude_columns else 'None'}")
    print(f"Detection threshold: {args.threshold}")

    analyzer = CSVAnalyzer()
    analyzer_results = analyzer.analyze_csv(
        args.csv_file,
        language=args.language,
        keys_to_skip=args.exclude_columns,
        threshold=args.threshold
    )
    print("\nAnalysis Results:")
    pprint.pprint(analyzer_results)

    anonymizer = BatchAnonymizerEngine()
    anonymized_results = anonymizer.anonymize_dict(analyzer_results)
    print("\nAnonymized Results:")
    pprint.pprint(anonymized_results)

    # Write anonymized results to output CSV file
    write_dict_to_csv(anonymized_results, args.output_file)
    print(f"\nAnonymized data written to: {args.output_file}")
