from snippets.fetch_account_balance import fetch_account_balance


def test_invalid_pv_ip_passed():

    success, message = fetch_account_balance(pv_ip="sdf",
                                             account_number="3bcaf9f2c4ea956ab2f991a0d4a7e0af82fa751f85fdc5a76a924101fdf1057c")

    assert success == False
    assert message == "A Connection error occurred."


def test_invalid_response_code():
    pass


def test_account_not_initialized():

    success, message = fetch_account_balance(pv_ip="52.52.160.149",
                                             account_number="12ba58dde332d47647a2edf955c85c11cb2a9a2f4b896121514b53c10a422c45")

    assert success == False
    assert message == "Account not initialized."


def test_valid_function_call():

    success, message = fetch_account_balance(pv_ip="52.52.160.149",
                                             account_number="12ba58dde332d47647a2edf955c85c11cb2a942f4b896121514b53c10a422c45")

    assert success == True
    assert message == "1"


