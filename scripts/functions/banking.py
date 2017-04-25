from scripts.functions.setup import get_api_connection, config


def get_account_info(account_id=''):
    """Retrieves information for a specific bank account. 
    Retrieves information about all accounts if no account_id is specified
    
    :param account_id: The id of a specific bank account  
    :return: Returns the information of 'MonetaryAccountBank' entries in JSON format
    """
    bunq_api = get_api_connection()
    user_id = config.get('USER_ID')

    r = bunq_api.query('user/' + user_id + '/monetary-account-bank/' + account_id, verify=True)
    if r.status_code == 200:
        return [x for x in r.json()['Response'] if list(x)[0] == 'MonetaryAccountBank']
    else:
        print('Get Account Info Error: ' + str(r.json()['Error'][0]))


def get_user_balances():
    """Retrieves information about all accounts for the user id specified in config
    
    :return: Prints out the balances of all accounts retrieved from the Bunq API
    """
    accounts = get_account_info()
    for entry in accounts:
        acc = entry['MonetaryAccountBank']
        print('%s - %s: %s %s' % (
            acc['id'],
            acc['description'],
            acc['balance']['value'],
            acc['balance']['currency']
        ))


def add_callback(account_id, category='MUTATION', clear=False):
    """Adds a Callback to a specific account
    Ref: https://doc.bunq.com/api/1/page/callbacks
    
    :param account_id: The id of the account. Call get_user_balances() to get the id. 
    :param category: The category of the event for which a callback should be added. 
    :param clear: Whether to clear all callbacks from the account or not. Default: False
    :return: Returns a success message or the Error message if request code not 200. 
    """
    bunq_api = get_api_connection()
    user_id = config.get('USER_ID')

    payload = {'notification_filters': []}
    if not clear:
        payload = {
            'notification_filters': [
                {
                    "notification_delivery_method": "URL",
                    "notification_target": config.get('CALLBACK_URI'),
                    "category": category
                }
            ]
        }
    r = bunq_api.query('user/' + user_id + '/monetary-account-bank/' + str(account_id), verify=True, method='PUT', payload=payload)
    if r.status_code == 200:
        print('Callback added successfully.')
    else:
        print('Add Callback Error: ' + str(r.json()['Error'][0]))


