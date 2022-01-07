'''
Third Party library required:
requests: python -m pip install requests


'''
import requests


def check_for_confirmation(*, bank_ip, block_signature):

    success = False  # Flag to check if the operation was successful.
    message = ""

    confirmation_check_url = f"http://{bank_ip}/confirmation_blocks?block=&block__signature={block_signature}"

    try:

        response = requests.get(confirmation_check_url)

        if response.status_code == 200:
            if response.json()["count"] > 0:
                success = True
                message = "Transaction confirmed!"
            else:
                message = "Transaction not confirmed!"

        else:
            message = "{'error': 'Code: %s.'}" % response.status_code

	# Handling requests excpetions gracefully
    except requests.exceptions.Timeout:
        message =  "{'error': 'The request timed out.'}"

    except requests.exceptions.ConnectionError:
        message =  "{'error': 'A Connection error occurred.'}"

    except requests.exceptions.HTTPError:
        message =  "{'error': 'An HTTP error occurred.'}"

    except requests.exceptions.RequestException as exception:
        message =  "{'error': 'Error while trying to connect to bank: %s'}" % exception

    return success, message

print(check_for_confirmation(bank_ip="45.56.92.194", block_signature="8adc553962e9dad5c0f5f130449ee59795224cd6bee2e463cbb9439904f59ab8e4f28aeb67bf9eec1d175989620b2b4aa6160fdb2bbe2974444c0f5ac469b40e"))
