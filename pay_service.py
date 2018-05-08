# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
from flask import abort, redirect, url_for
from uuid import uuid4 as uuid
import hashlib
import requests
import logging
from settings import PREFIX_TO_URL, SHOP_ID, SECRET_KEY, PAYER_CURRENCY, PAYWAY
import constant

app = Flask(__name__)

logging.basicConfig(filename="logs/pay_service.log", level=logging.INFO)

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
    logging.info("Data for form: %s", _args)
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
    logging.info("Data for form: %s", _args)
    res = requests.post(constant.URL_FOR_BILL, json=_args)
    if res.status_code == 200:
        data = res.json()
        logging.info("Response: %s", data)
        if data[constant.RESULT]:
            action = redirect(data[constant.DATA][constant.URL])
        else:
            logging.info("ERROR: %s", data[constant.MESSAGE])
            action = render_template(
                'error_page.html',
                error_code=data[constant.ERROR_CODE],
                message=data[constant.MESSAGE]
            )
    else:
        logging.info("ERROR: unknown error")
        action = render_template('error_page.html')
    return action

def invoice(data):
    _args = {
        constant.AMOUNT: data[constant.AMOUNT],
        constant.CURRENCY: constant.CURRENCY_VALUE[data[constant.CURRENCY]],
        constant.PAYWAY: PAYWAY,
        constant.SHOP_ID: SHOP_ID,
        constant.SHOP_ORDER_ID: str(uuid())
    }
    _args[constant.SIGN] = sign(constant.REQUIRED_INVOICE_KEYS, _args)
    logging.info("Data for form: %s", _args)
    res = requests.post(constant.URL_FOR_INVOICE, json=_args)
    if res.status_code == 200:
        data = res.json()
        logging.info("Response: %s", data)
        if data[constant.RESULT]:
            action =render_template("invoice.html", data=data[constant.DATA])
        else:
            logging.info("ERROR: %s", data[constant.MESSAGE])
            action = render_template(
                'error_page.html',
                error_code=data[constant.ERROR_CODE],
                message=data[constant.MESSAGE]
            )
    else:
        logging.info("ERROR: unknown error")
        action = render_template('error_page.html')
    return action

@app.route(PREFIX_TO_URL + "/test_market")
def start_page():
    return render_template('start_page.html', prefix=PREFIX_TO_URL)

@app.route(PREFIX_TO_URL + "/service", methods=["GET", "POST"])
def service():
    logging.info("Data from form: %s", request.form)
    currency = request.form[constant.CURRENCY]
    if not request.form[constant.AMOUNT]:
        logging.info("ERROR: %s", constant.MESSAGE_AMOUNT_EMPTY)
        return render_template("error_page.html",
                               message=constant.MESSAGE_AMOUNT_EMPTY)
    if currency == constant.EUR:
        return pay(request.form)
    elif currency == constant.USD:
        return bill(request.form)
    elif currency == constant.RUB:
        return invoice(request.form)
    else:
        logging.info("ERROR: unknown error")
        return render_template("error_page.html")


if __name__ == "__main__":
    app.run()

