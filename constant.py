# -*- coding: utf-8 -*-


AMOUNT = 'amount'
CURRENCY = 'currency'
PAYER_CURRENCY = 'payer_currency'
SHOP_CURRENCY = 'shop_currency'
SHOP_AMOUNT = 'shop_amount'
DESCRIPTION = 'description'
PAYWAY = 'payway'
SHOP_ID = 'shop_id'
SHOP_ORDER_ID = 'shop_order_id'
SIGN = 'sign'
URL = 'url'
DATA = 'data'
RESULT = 'result'
ERROR_CODE = 'error_code'
MESSAGE = 'message'
RUB = 'RUB'
EUR = 'EUR'
USD = 'USD'
REQUIRED_PAY_KEYS = [AMOUNT, CURRENCY, SHOP_ID, SHOP_ORDER_ID]
REQUIRED_BILL_KEYS = [
    SHOP_AMOUNT, SHOP_CURRENCY, SHOP_ID, SHOP_ORDER_ID, PAYER_CURRENCY
]
REQUIRED_INVOICE_KEYS = [AMOUNT, CURRENCY, PAYWAY, SHOP_ID, SHOP_ORDER_ID]
CURRENCY_VALUE = {RUB: 643, EUR: 978, USD: 840}
URL_FOR_BILL = "https://core.piastrix.com/bill/create"
URL_FOR_INVOICE = "https://core.piastrix.com/invoice/create"
MESSAGE_AMOUNT_EMPTY = "The amount field can not be empty."

