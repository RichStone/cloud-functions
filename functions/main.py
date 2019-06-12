from google.cloud import storage
import json


def get_verified_data():
    """
    Verified data could be aggregated from analysis of previous invoices in the Cloud Storage.

    :return: dictionary - dummy data of verified data per building
    """
    return {
        'building_id': '139498',
        'building_address': '7 Arkansas Hill',
        'floors_amount': 8,
        'typical_cost': [
            {
                'type': 'energy',
                'min': 22000,
                'max': 29000,
                'median': 26000,
                'mean': 25555
            },
            {
                'type': 'gardening',
                'min': 1000,
                'max': 3000,
                'median': 1500,
                'mean': 2000
            }
        ],
        'contracts': [
            {
                'type': 'energy',
                'contractor': 'E.ON',
                'date_from': '2015-01-01',
                'date_to': '2022-31-12',
                'contract_cancelled': False
            }
        ]
    }


def verify_invoices(request):
    def is_correct_address():
        """
        Address on invoice must match address of building
        :return: boolean
        """
        pass

    def is_inside_floor_range():
        """
        Floor number on invoice cannot not be greater or smaller than the amount of floors
        :return: boolean
        """
        pass

    def is_severe_outlier(threshold_percent=100):
        """
        Anomalies that surpass the min or max by a high percentage should be reported immediately
        :param threshold_percent:
        :return: boolean
        """
        pass

    def is_mild_outlier(threshold_percent=50):
        """
        Anomalies within a reasonable percentage from the mean must be reported in aggregate to the accounting deparment.
        :param threshold_percent:
        :return: boolean
        """
        pass

    def issue_date_is_after_invoice_period():
        """
        The issue date of the invoice cannot be before or inside the accounting period
        :return: boolean
        """
        pass

    def invoice_period_is_inside_contract_period():
        """
        The invoice period has to be inside the contract period
        :return: boolean
        """
        pass

    client = storage.Client()
    bucket = client.get_bucket('tukdata')

    building_raw_data = bucket.get_blob('mini-buildings.json').download_as_string()
    invoices_raw_data = bucket.get_blob('mini-sample-invoices.json').download_as_string()

    building = json.loads(building_raw_data)
    invoices = json.loads(invoices_raw_data)

    verified_data = get_verified_data()

    return building, invoices
