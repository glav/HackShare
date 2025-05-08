import csv
from typing import List, Dict, Any


class CatalogDataReader:
    """
    A class to read and manage catalog data from a CSV file.
    """

    def __init__(self):
        """
        Initialize the CatalogDataReader with an empty catalog items list.
        """
        self.catalog_items = []

    def read_catalog_csv(self, file_path: str) -> None:
        """
        Read catalog data from a CSV file and store it in the internal catalog_items list.

        Args:
            file_path (str): Path to the CSV file containing catalog data.

        The CSV file should have the following columns:
        - Category
        - Catalog Item Name
        - Catalog Item Short Description
        - Catalog Item Description
        """
        try:
            self.catalog_items = []  # Reset the catalog items list

            with open(file_path, 'r', encoding='utf-8') as csv_file:
                csv_reader = csv.DictReader(csv_file)

                # Verify that the CSV file has the required columns
                required_columns = [
                    'Category',
                    'Catalog Item Name',
                    'Catalog Item Short Description',
                    'Catalog Item Description'
                ]

                for column in required_columns:
                    if column not in csv_reader.fieldnames:
                        raise ValueError(f"CSV file is missing required column: {column}")

                # Read each row into the catalog_items list
                for row in csv_reader:
                    self.catalog_items.append({
                        'category': row['Category'],
                        'name': row['Catalog Item Name'],
                        'short_description': row['Catalog Item Short Description'],
                        'description': row['Catalog Item Description']
                    })

            return self.catalog_items

        except Exception as e:
            print(f"Error reading catalog CSV file: {e}")
            return []

    def get_catalog_items(self) -> List[Dict[str, Any]]:
        """
        Get all catalog items that have been loaded.

        Returns:
            List[Dict[str, Any]]: List of catalog items, each as a dictionary.
        """
        return self.catalog_items

    def get_catalog_items_by_category(self, category: str) -> List[Dict[str, Any]]:
        """
        Get catalog items filtered by category.

        Args:
            category (str): Category name to filter by.

        Returns:
            List[Dict[str, Any]]: List of catalog items in the specified category.
        """
        return [item for item in self.catalog_items if item['category'].lower() == category.lower()]
