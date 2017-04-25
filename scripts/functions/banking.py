from scripts.functions.setup import get_api_connection, config


def get_user_balances():
    """Retrieves information about all accounts for the user id specified in config
    
    :return: Prints out the balances of all accounts retrieved from the Bunq API
    """
    bunq_api = get_api_connection()
    user_id = config.get('USER_ID')

    r = bunq_api.query('user/%s/monetary-account-bank' % user_id, verify=True)
    if r.status_code == 200:
        acc_type = 'MonetaryAccountBank'
        res = [x for x in r.json()['Response'] if list(x)[0] == acc_type]
        for entry in res:
            acc = entry[acc_type]
            print('%s: %s %s' % (
                acc['description'],
                acc['balance']['value'],
                acc['balance']['currency']
            ))
    else:
        print('Retrieve Account Balances Error: ' + str(r.json()['Error'][0]))


