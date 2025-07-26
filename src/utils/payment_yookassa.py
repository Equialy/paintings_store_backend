import yookassa
import uuid

from yookassa import Payment
from src.settings import settings


yookassa.Configuration.account_id = settings.payment.account_id_yookassa
yookassa.Configuration.secret_key = settings.payment.secret_key_yookassa


async def yk_create(amount, user_id):
    id_key = str(uuid.uuid4())
    payment = Payment.create(
        {
            "amount": {"value": str(amount), "currency": "RUB"},
            "payment_method_data": {"type": "bank_card"},
            "confirmation": {
                "type": "redirect",
                "return_url": "http://127.0.0.1:3000/",
            },
            "capture": True,
            "metadata": {"user_id": user_id},
            "description": "Описание товара....",
        },
        id_key,
    )

    return payment.confirmation.confirmation_url, payment.id


async def check_payment(payment_id):
    payment = yookassa.Payment.find_one(payment_id)
    if payment.status == "succeeded":
        return payment.metadata
    else:
        return False
