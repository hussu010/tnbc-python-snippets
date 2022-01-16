'''
Required third party library
requests: python -m pip install requests


'''
import requests

def fetch_incoming_transactions(*, bank_ip, account_number):

    success = False
    message = ""

    account_transactions_url = f"http://{bank_ip}/bank_transactions?recipient={account_number}"

    try:
        
        response = requests.get(account_transactions_url)

        if response.status_code == 200:
            message = str(response.json())

        else:
            message = response.status_code
            
    except requests.exceptions.Timeout:
        message = "The request timed out."

    except requests.exceptions.ConnectionError:
        message = "A Connection error occurred."
        
    except requests.exceptions.HTTPError:
        message = "An HTTP error occurred."

    except requests.exceptions.RequestException as exception:
        message = exception

    return success, message

print(fetch_incoming_transactions(bank_ip="54.183.16.194", account_number="22d0f0047b572a6acb6615f7aae646b0b96ddc58bfd54ed2775f885baeba3d6a"))
