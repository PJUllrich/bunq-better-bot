import email
import json
from io import StringIO

_IBAN_SAVINGS_ACCOUNT = 'NL88BUNQ9900046528'


def handle_event(msg_bytes_tuple):
    msg_json = parse_message(msg_bytes_tuple[0])
    category = msg_json['NotificationUrl']['category']
    if category == 'MUTATION':
        handle_mutation(msg_json)
    else:
        print('No handler found for category: ' + category)


def parse_message(raw):
    raw_string = raw[0].decode('UTF-8')
    request_line, headers_alone = raw_string.split('\r\n', 1)
    message = email.message_from_file(StringIO(headers_alone))
    payload = message.get_payload().split("'")[0]
    return json.loads(payload)


def handle_mutation(msg_json):
    payment = msg_json['NotificationUrl']['object']['Payment']
    amount = payment['amount']
    if amount['currency'] == 'EUR':
        amount_to_save = 0.50 - (amount['value'] % 0.50)
        iban_to_deduct = payment['counterparty_alias']['iban']
        iban_savings = _IBAN_SAVINGS_ACCOUNT
        print(str(amount_to_save) + ' from ' + iban_to_deduct + ' to ' + iban_savings)
    else:
        print('Handle Mutation Info: Currency is not Euro. Doing nothing.')
