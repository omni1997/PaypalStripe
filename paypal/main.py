import os
import pytest
import paypalrestsdk

# Test configuration
paypalrestsdk.configure({
    "mode": "sandbox",
    "client_id": "fake_client_id",
    "client_secret": "fake_client_secret"
})

def create_payment():
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "credit_card",
            "funding_instruments": [{
                "credit_card": {
                    "type": "visa",
                    "number": "4111111111111111",
                    "expire_month": "12",
                    "expire_year": "2025",
                    "cvv2": "123",
                    "first_name": "Test",
                    "last_name": "User"
                }
            }]
        },
        "transactions": [{
            "amount": {
                "total": "10.00",
                "currency": "USD"
            },
            "description": "Test payment"
        }]
    })
    return payment.create()

def test_payment_valid(mocker):
    mocker.patch('paypalrestsdk.Payment.create', return_value=True)
    result = create_payment()
    assert result is True

def test_payment_insufficient_funds(mocker):
    mocker.patch(
        'paypalrestsdk.Payment.create',
        side_effect=paypalrestsdk.ResourceNotFound({'name': 'INSUFFICIENT_FUNDS'})
    )
    with pytest.raises(paypalrestsdk.ResourceNotFound):
        create_payment()

def test_payment_card_unknown(mocker):
    mocker.patch(
        'paypalrestsdk.Payment.create',
        side_effect=paypalrestsdk.ResourceNotFound({'name': 'CARD_REFUSED'})
    )
    with pytest.raises(paypalrestsdk.ResourceNotFound):
        create_payment()
