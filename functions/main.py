from google.cloud import storage
import json
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os
import logging


def get_verified_data():
    """
    Verified data could be aggregated from analysis of previous invoices in the Cloud Storage.

    :return: dictionary - dummy data of verified data per building
    """
    return {
        'building_id': '139498',
        'building_address': '7 Arkansas Hill',
        'min_floor': -2,
        'max_floor': 8,
        'typical_cost': [
            {
                'type': 'energy',
                'min': 22000,
                'max': 3000,
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


def send_alert_message(message_html='default text'):
    message = Mail(
        from_email='from_email@example.com',
        to_emails='richard.has.fun@gmail.com',
        subject='Sending with Twilio SendGrid is Fun',
        html_content=message_html)
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        logging.info(response.status_code)
        logging.info(response.body)
        logging.info(response.headers)
    except Exception as e:
        logging.info(str(e))


def verify_invoices(request):
    try:
        from cStringIO import StringIO
    except ImportError:
        from io import StringIO

    log_stream = StringIO()
    logging.basicConfig(stream=log_stream, level=logging.INFO)

    def is_correct_address():
        """
        Address on invoice must match address of building
        :return: boolean
        """
        if invoices[0]['BuildingAddress'] == verified_data['building_address']:
            return True
        else:
            return False

    def is_inside_floor_range():
        """
        Floor number on invoice cannot not be greater or smaller than the amount of floors
        :return: boolean
        """
        try:
            if invoices[0]['BuildingFloor'] >= verified_data['min_floor'] and invoices[0]['BuildingFloor'] <= verified_data['max_floor']:
                return True
            else:
                return False
        except TypeError:
            # TODO: handle floor specific or wrongly written floors
            logging.info('Type missmatch, either the floor was not written as int or the invoicing is not floor specific')
            return False

    def is_severe_outlier(threshold_percent=0.5):
        """
        Anomalies that surpass the max of verified data by a high percentage should be reported immediately
        :param threshold_percent:
        :return: boolean
        """
        verified_max = verified_data['typical_cost'][0]['max']
        invoice_sum = invoices[0]['PaymentSum']
        allowed_surpass = verified_max * threshold_percent
        current_discrepancy = invoice_sum - verified_max

        if current_discrepancy > allowed_surpass:
            logging.info('The discrepancy {} between verified max {} and the payment sum {} is too high'
                  .format(current_discrepancy, verified_max, invoice_sum))
            return True
        else:
            return False

    def is_mild_outlier(threshold_percent=0.5):
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

    def execute_verification():

        formal_verifications = [
            is_correct_address(),
            is_inside_floor_range(),
        ]
        if False in formal_verifications:
            # TODO: send to manual
            logging.info('send for manual correction')

        if is_severe_outlier():
            # TODO: send immediate message
            logging.info('attention')
            logging.info('notify accountant clarification')
        elif is_mild_outlier():
            # TODO: aggregate and send message
            logging.info('look into it')
        else:
            logging.info('no outliers detected 👍')

    client = storage.Client()
    bucket = client.get_bucket('tukdata')

    building_raw_data = bucket.get_blob('mini-buildings.json').download_as_string()
    invoices_raw_data = bucket.get_blob('mini-sample-invoices.json').download_as_string()

    building = json.loads(building_raw_data)
    invoices = json.loads(invoices_raw_data)
    verified_data = get_verified_data()

    execute_verification()

    return log_stream.getvalue()


if __name__ == '__main__':
    s = verify_invoices(dict)
    logging.info(s)
