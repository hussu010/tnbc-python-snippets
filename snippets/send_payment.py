'''
Required third party libraries
- requests: python -m pip install requests
- PyNaCl: pip install pynacl


'''

import requests
import json

from nacl.encoding import HexEncoder
import nacl.signing

from operator import itemgetter


# Utils
def generate_block(balance_lock, transactions, signing_key):
    account_number = signing_key.verify_key.encode(encoder=HexEncoder).decode('utf-8')
    message = {
        'balance_key': balance_lock,
        'txs': sorted(transactions, key=itemgetter('recipient'))
    }
    signature = signing_key.sign(json.dumps(message, separators=(',', ':'), sort_keys=True).encode('utf-8')).signature.hex()
    block = {
        'account_number': account_number,
        'message': message,
        'signature': signature
    }
    return json.dumps(block)


def is_valid_key(key):

    # Check if signing key is valid hexadecimal
    try:
        int(key, 16)

    except ValueError as exception:
        return False

    # Check if the length of the key is 64
    if len(key) != 64:
        return False

    return True


# -------------------------------------------------------------------

def send_tnbc(*, bank_ip, signing_key, destination_account_number, amount, memo):

    success = False
    message = ""

    if not is_valid_key(signing_key):
        message = "{'error': 'Invalid Signing Key.'}"
        return success, message
    
    if not is_valid_key(destination_account_number):
        message = "{'error': 'Invalid destination account number.'}"
        return success, message

    nacl_signing_key = nacl.signing.SigningKey(str.encode(signing_key), encoder=nacl.encoding.HexEncoder)
    payment_account_number = nacl_signing_key.verify_key.encode(encoder=nacl.encoding.HexEncoder).decode('utf-8')

    try:
        bank_config_url = f'http://{bank_ip}/config?format=json'
        bank_config = requests.get(bank_config_url).json()

        balance_lock_url = f"{bank_config['primary_validator']['protocol']}://{bank_config['primary_validator']['ip_address']}:{bank_config['primary_validator']['port'] or 0}/accounts/{payment_account_number}/balance_lock?format=json"
        balance_lock = requests.get(balance_lock_url).json()['balance_lock']

    # Handling bank config and balance lock exceptions gracefully.
    except requests.exceptions.Timeout:
        message =  "{'error': 'The request timed out while trying to retrieve bank config.'}"
        return success, message

    except requests.exceptions.ConnectionError:
        message =  "{'error': 'Connection error occurred while trying to retrieve bank config.'}"
        return success, message
        
    except requests.exceptions.HTTPError:
        message =  "{'error': 'An HTTP error occurred while trying to retrieve bank config.'}"
        return success, message

    except requests.exceptions.RequestException as exception:
        message =  "{'error': 'Error while trying to retrieve bank config: %s'}" % exception
        return success, message

    # Check if the signing key is initialized. If not, request the user to initialize by sending a tnbc.
    if not balance_lock:
        message =  "{'error': 'Signing key not initialized. Please send a tnbc to the corresponding account number to initialize.'}"
        return success, message

    # Creating a transaction to generate a block.
    txs = [
        {
            'amount': amount,
            'memo': memo,
            'recipient': destination_account_number,
        },
        {
            'amount': int(bank_config['default_transaction_fee']),
            'fee': 'BANK',
            'recipient': bank_config['account_number'],
        },
        {
            'amount': int(bank_config['primary_validator']['default_transaction_fee']),
            'fee': 'PRIMARY_VALIDATOR',
            'recipient': bank_config['primary_validator']['account_number'],
        }
    ]

    # generate a transaction block with transaction info.
    data = generate_block(balance_lock, txs, nacl_signing_key)

    headers = {
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) TNBAccountManager/1.0.0-alpha.43 Chrome/83.0.4103.122 Electron/9.4.0 Safari/537.36',
        'Content-Type': 'application/json',
    }

    try:

        response = requests.post(f'http://{bank_ip}/blocks', headers=headers, data=data)

        if response.status_code == 201:
            success = True
            message = response.json()

        else:
            message = response

    # Handling block exceptions gracefully.
    except requests.exceptions.Timeout:
        message =  "{'error': 'The request timed out while trying to create a block.'}"
        return success, message

    except requests.exceptions.ConnectionError:
        message =  "{'error': 'A Connection error occurred while trying to create a block.'}"
        return success, message

    except requests.exceptions.HTTPError:
        message =  "{'error': 'An HTTP error occurred while trying to create a block.'}"
        return success, message

    except requests.exceptions.RequestException as exception:
        message =  "{'error': 'Error while trying to create a block: %s'}" % exception
        return success, message

    return success, message


print(send_tnbc(bank_ip="BANK_IP", signing_key="SIGNING_KEY", destination_account_number="DESTINATION_ACCOUNT_NUMBER", amount=1, memo="MEMO"))
