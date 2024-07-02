import json, os
from constants import DATA_FOLDER

def load_file(file_name):
    file_path = os.path.join(DATA_FOLDER, file_name)
    return json.load(open(file_path))


def test_load_file():
    from pprint import pprint 

    file_name = "__utah-businesses-for-sale__3__.json"
    results = load_file(file_name)
    pprint(results)


import json, os, csv
from constants import DATA_FOLDER
import unittest
from google.cloud import bigquery

# Replace with your project ID, dataset ID, and table ID
project_id = 'your-project-id'
dataset_id = 'your-dataset-id'
table_id = 'your-table-id'

# Replace with the path to your CSV file
csv_file_path = 'path/to/your/file.csv'

def load_file(file_name):
    """Loads a JSON file from the DATA_FOLDER.

    Args:
        file_name: The name of the JSON file to load.

    Returns:
        The contents of the JSON file as a Python dictionary.
    """
    file_path = os.path.join(DATA_FOLDER, file_name)
    return json.load(open(file_path))

def upload_to_bigquery(csv_file_path, project_id, dataset_id, table_id):
    """Uploads a CSV file to a BigQuery table.

    Args:
        csv_file_path: The path to the CSV file.
        project_id: The ID of the Google Cloud project.
        dataset_id: The ID of the BigQuery dataset.
        table_id: The ID of the BigQuery table.
    """
    client = bigquery.Client()
    table_ref = client.dataset(dataset_id).table(table_id)

    with open(csv_file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        rows = list(reader)

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,  # Skip the header row
        autodetect=True,  # Automatically infer the schema from the CSV file
    )
    job = client.load_table_from_json(rows, table_ref, job_config=job_config)
    job.result()

    print(f"Loaded {len(rows)} rows into {table_ref}")

class TestSaveToStorage(unittest.TestCase):

    def test_load_file(self):
        """Tests the load_file function."""
        file_name = "__utah-businesses-for-sale__3__.json"
        results = load_file(file_name)
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)

    def test_upload_to_bigquery(self):
        """Tests the upload_to_bigquery function."""
        # This test will not actually upload data to BigQuery.
        # You will need to replace the placeholders with your actual values
        # and run the test in an environment with access to BigQuery.
        csv_file_path = 'path/to/your/file.csv'
        project_id = 'your-project-id'
        dataset_id = 'your-dataset-id'
        table_id = 'your-table-id'
        upload_to_bigquery(csv_file_path, project_id, dataset_id, table_id)


if __name__ == "__main__":

    test_load_file()
