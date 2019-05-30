from google.cloud import storage
import json
import os


def verify_invoices():
    service_key_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    client = storage.Client.from_service_account_json(service_key_path)
    bucket = client.get_bucket('tukdata')

    building_raw_data = bucket.get_blob('mini-buildings.json').download_as_string()
    invoices_raw_data = bucket.get_blob('mini-sample-invoices.json').download_as_string()

    building = json.loads(building_raw_data)
    invoices = json.loads(invoices_raw_data)

    return building, invoices
