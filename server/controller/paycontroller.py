from phonepe.sdk.pg.payments.v1.payment_client import PhonePePaymentClient
from phonepe.sdk.pg.env import Env

merchant_id = "YOUR_MERCHANT_ID"
salt_key = "YOUR_SALT_KEY"
salt_index = 1
env = Env.UAT # Change to Env.PROD when you go live

phonepe_client = PhonePePaymentClient(merchant_id=merchant_id, salt_key=salt_key, salt_index=salt_index, env=env)
