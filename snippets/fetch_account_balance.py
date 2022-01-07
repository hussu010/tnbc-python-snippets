'''
Library Required: requests
Installation of request: `python -m pip install requests`
'''

import requests


def fetch_account_balance(*, pv_ip, account_number):

    success = False
    message = ""

    pv_balance_endpoint = f"http://{pv_ip}/accounts/{account_number}/balance"

    try:
        
        response = requests.get(pv_balance_endpoint)

        if response.status_code == 200:

            balance = str(response.json()["balance"])

            if balance == "None":
                message = "Account not initialized."
            else:    
                success = True
                message = str(response.json()["balance"])
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


print(fetch_account_balance(pv_ip="sdf", account_number="3bcaf9f2c4ea956ab2f991a0d4a7e0af82fa751f85fdc5a76a924101fdf1057c"))
