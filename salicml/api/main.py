import logging
import sys

import numpy
from flask import Flask, jsonify
from flask.json import JSONEncoder

from salicml.middleware.middleware import Middleware
from salicml.utils.utils import is_valid_pronac


class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):
        if isinstance(obj, numpy.bool_):
            return 'True' if obj else 'False'

        return super(CustomJSONEncoder, self).default(obj)


app = Flask(__name__)
app.json_encoder = CustomJSONEncoder
app.config['JSON_AS_ASCII'] = False

handler = logging.StreamHandler(sys.stdout)
app.logger.addHandler(handler)
app.logger.setLevel(logging.DEBUG)

app.middleware = Middleware()
app.middleware.load_all()


@app.route('/metric/number_of_items/<string:pronac>', methods=['GET'])
def get_metric_number_of_items(pronac):
    if is_valid_pronac(pronac):
        result = app.middleware.get_metric_number_of_items(pronac)
        return jsonify(result), 200
    else:
        INVALID_PRONAC_MESSAGE = 'Invalid PRONAC'
        return jsonify(INVALID_PRONAC_MESSAGE), 400
