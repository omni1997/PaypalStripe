import pytest
import stripe

# Test configuration
stripe.api_key = "sk_test_fake_api_key"

def create_payment():
    try:
        # Simulate a charge creation (replace this with actual Stripe API call in real usage)
        charge = stripe.Charge.create(
            amount=1000,  # Amount in cents
            currency="usd",
            source="tok_visa",  # A fake token for testing
            description="Test payment"
        )
        return charge
    except stripe.error.StripeError as e:
        return e

def test_payment_valid(mocker):
    mocker.patch('stripe.Charge.create', return_value={"id": "ch_fake_id", "status": "succeeded"})
    result = create_payment()
    assert result["status"] == "succeeded"

def test_payment_insufficient_funds(mocker):
    mocker.patch(
        'stripe.Charge.create',
        side_effect=stripe.error.CardError(
            "Insufficient funds",
            param='source',
            code='insufficient_funds'
        )
    )
    result = create_payment()
    assert isinstance(result, stripe.error.CardError)
    assert result.code == 'insufficient_funds'

def test_payment_card_unknown(mocker):
    mocker.patch(
        'stripe.Charge.create',
        side_effect=stripe.error.CardError(
            "Card refused",
            param='source',
            code='card_declined'
        )
    )
    result = create_payment()
    assert isinstance(result, stripe.error.CardError)
    assert result.code == 'card_declined'
