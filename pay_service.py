# -*- coding: utf-8 -*-

from flask import Flask, render_template, request
from uuid import uuid4 as uuid
import hashlib
from settings import PREFIX_TO_URL, SHOP_ID, SECRET_KEY
import constant

app = Flask(__name__)


def sign(required_keys, _args):
    return hashlib.sha256(str.encode(
        ':'.join([str(_args[i]) for i in sorted(required_keys)]) +
        SECRET_KEY)).hexdigest()

@app.route(PREFIX_TO_URL + "/test_market")
def start_page():
    return render_template('start_page.html', prefix=PREFIX_TO_URL)

@app.route(PREFIX_TO_URL + "/service/pay", methods=["GET", "POST"])
def pay():
    _args = {constant.AMOUNT: float(request.form[constant.AMOUNT]),
            constant.CURRENCY: constant.CURRENCY_VALUE[
                request.form[constant.CURRENCY]],
            constant.DESCRIPTION: request.form[constant.DESCRIPTION],
            constant.SHOP_ID: SHOP_ID,
            constant.SHOP_ORDER_ID: uuid()}
    _args[constant.SIGN] = sign(constant.REQUIRED_PAY_KEYS, _args)
    print(_args)
    return render_template('pay.html', _args=_args)


if __name__ == "__main__":
    app.run()

