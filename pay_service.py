# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
from flask import abort, redirect, url_for
from uuid import uuid4 as uuid
import hashlib
import requests
from settings import PREFIX_TO_URL, SHOP_ID, SECRET_KEY, PAYER_CURRENCY
import constant

app = Flask(__name__)


def sign(required_keys, _args):
    return hashlib.sha256(str.encode(
        ':'.join([str(_args[i]) for i in sorted(required_keys)]) +
        SECRET_KEY)).hexdigest()

def pay(data):
    _args = {
        constant.AMOUNT: data[constant.AMOUNT],
        constant.CURRENCY:
            constant.CURRENCY_VALUE[data[constant.CURRENCY]],
        constant.DESCRIPTION: data[constant.DESCRIPTION],
        constant.SHOP_ID: SHOP_ID,
        constant.SHOP_ORDER_ID: str(uuid())
    }
    _args[constant.SIGN] = sign(constant.REQUIRED_PAY_KEYS, _args)
    return render_template('pay.html', _args=_args)

def bill(data):
    _args = {
        constant.PAYER_CURRENCY: constant.CURRENCY_VALUE[PAYER_CURRENCY],
        constant.SHOP_AMOUNT: data[constant.AMOUNT],
        constant.SHOP_CURRENCY:
            constant.CURRENCY_VALUE[data[constant.CURRENCY]],
        constant.SHOP_ID: SHOP_ID,
        constant.SHOP_ORDER_ID: str(uuid())
    }
    _args[constant.SIGN] = sign(constant.REQUIRED_BILL_KEYS, _args)
    res = requests.post(constant.URL_FOR_BILL, json=_args)
    if res.status_code == 200:
        data = res.json()
        if data[constant.RESULT]:
            action = redirect(data[constant.DATA][constant.URL])
        else:
            action = render_template(
                'error_page.html',
                error_code=data[constant.ERROR_CODE],
                message=data[constant.MESSAGE]
            )
    else:
        action = render_template('error_page.html')
    return action

@app.route(PREFIX_TO_URL + "/test_market")
def start_page():
    return render_template('start_page.html', prefix=PREFIX_TO_URL)

@app.route(PREFIX_TO_URL + "/service", methods=["GET", "POST"])
def service():
    currency = request.form[constant.CURRENCY]
    if currency == constant.EUR:
        return pay(request.form)
    elif currency == constant.USD:
        return bill(request.form)
    else:
        return "test"


if __name__ == "__main__":
    app.run()

