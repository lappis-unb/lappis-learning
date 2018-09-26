import logging
import sys

import numpy
from flask import Flask, jsonify
from flask.json import JSONEncoder

from salicml.middleware.middleware import Middleware


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

middleware = Middleware()
middleware.load_all()


@app.route('/metric/number_of_items/<int:pronac>', methods=['GET'])
def get_metric_number_of_items(pronac):
    result = middleware.get_metric_number_of_items(pronac)
    return jsonify(result), 200
