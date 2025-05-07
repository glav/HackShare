import csv
import pprint
import argparse
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
    --language      Language for PII detection (default: 'en')
    --exclude-columns  List of column names to exclude from redaction

Examples:
    # Process the default CSV file
    python src/redact_pii.py

    # Process a specific CSV file
    python src/redact_pii.py --csv-file ./path/to/your/file.csv

    # Exclude specific columns from redaction
    python src/redact_pii.py --exclude-columns id city

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
            analyzer_results = self.analyze_dict(csv_dict, language, keys_to_skip)
            return list(analyzer_results)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Redact PII from CSV files")
    parser.add_argument(
        "--csv-file",
        type=str,
        default="./data/support_queries.csv",
        help="Path to the CSV file to analyze"
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
    args = parser.parse_args()

    print(f"Processing file: {args.csv_file}")
    print(f"Language: {args.language}")
    print(f"Excluding columns: {args.exclude_columns if args.exclude_columns else 'None'}")

    analyzer = CSVAnalyzer()
    analyzer_results = analyzer.analyze_csv(
        args.csv_file,
        language=args.language,
        keys_to_skip=args.exclude_columns
    )
    print("\nAnalysis Results:")
    pprint.pprint(analyzer_results)

    anonymizer = BatchAnonymizerEngine()
    anonymized_results = anonymizer.anonymize_dict(analyzer_results)
    print("\nAnonymized Results:")
    pprint.pprint(anonymized_results)
