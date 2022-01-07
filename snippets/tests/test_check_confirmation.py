from snippets.check_payment_confirmation import check_for_confirmation


def test_invalid_bank_ip():

	success, message = check_for_confirmation(bank_ip="InvalidIP",
											  block_signature="randomblocksignature")

	assert success == False
	assert message == "{'error': 'A Connection error occurred.'}"


def test_unconfirmed_transaction():

	success, message = check_for_confirmation(bank_ip="45.56.92.194",
											  block_signature="randomblocksignature")

	assert success == False
	assert message == "Transaction not confirmed!"

def test_confirmed_transaction():

	success, message = check_for_confirmation(bank_ip="45.56.92.194",
											  block_signature="18788fd80db75e72a33ab7b1581b6fbedeb7ecf2567edd05bc9b0ac6b0862c39f8a1e48f936a3aeb08ef0b85f992ac8e58f1c52ae36463701b33b885f468f208")

	assert success == True
	assert message == "Transaction confirmed!"
