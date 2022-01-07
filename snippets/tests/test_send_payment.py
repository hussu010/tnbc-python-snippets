from snippets.send_payment import send_tnbc


def test_invalid_signing_key():
    success, message = send_tnbc(bank_ip="BANK_IP",
                                 signing_key="zzzzzz",
                                 destination_account_number="DESTINATION_ACCOUNT_NUMBER",
                                 amount=1,
                                 memo="MEMO")
    assert success == False
    assert message == "{'error': 'Invalid Signing Key.'}"


def test_invalid_destination_account_number():
    success, message = send_tnbc(bank_ip="BANK_IP",
                                 signing_key="a8a5f2ad6012646e5a1ab7b1be97a40bd4e951d7c683db34c0f84624c9104eba",
                                 destination_account_number="random_xyz",
                                 amount=1,
                                 memo="MEMO")
    assert success == False
    assert message == "{'error': 'Invalid destination account number.'}"


def test_invalid_bank_ip():
    success, message = send_tnbc(bank_ip="BANK_IP",
                                 signing_key="a8a5f2ad6012646e5a1ab7b1be97a40bd4e951d7c683db34c0f84624c9104eba",
                                 destination_account_number="a8a5f2ad6012646e5a1ab7b1be97a40bd4e951d7c683db34c0f84624c9104eba",
                                 amount=1,
                                 memo="MEMO")
    assert success == False
    assert message == "{'error': 'Connection error occurred while trying to retrieve bank config.'}"


def test_balance_lock_not_available():
    success, message = send_tnbc(bank_ip="54.183.16.194",
                                 signing_key="a8a5f2ad6012646e5a1ab7b1be97a40bd4e951d7c683db34c0f84624c9104eba",
                                 destination_account_number="a8a5f2ad6012646e5a1ab7b1be97a40bd4e951d7c683db34c0f84624c9104eba",
                                 amount=1,
                                 memo="MEMO")
    assert success == False
    assert message == "{'error': 'Signing key not initialized. Please send a tnbc to the corresponding account number to initialize.'}"


def test_error_while_sending_block():
    pass


def test_correct_response_code_while_creating_block():
    pass


def test_sending_payment_success():
    pass
