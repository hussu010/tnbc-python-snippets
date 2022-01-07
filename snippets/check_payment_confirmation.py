'''
Third Party library required:
requests: python -m pip install requests


'''
import requests


def check_for_confirmation(*, bank_ip, block_signature):

    success = False  # Flag to check if the operation was successful.
    message = ""  # Variable that hosts the balance/ error message.

    confirmation_check_url = f"http://{bank_ip}/confirmation_blocks?block=&block__signature={block_signature}"

    try:

        response = requests.get(confirmation_check_url)

        if response.status_code == 200:
            success = True
            message = str(response.json()["count"])

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

print(check_for_confirmation(bank_ip="45.56.92.194", block_signature="b462e69d1e24699cf235c7e9ec8286e62a2571a96403e9a9e1cb28eec8b5e80ccd4a872cf66f38baa3b4daec70e864e08d152b35e8b14c33c1c2a878a04e8706"))
