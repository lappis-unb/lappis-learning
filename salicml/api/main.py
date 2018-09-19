import numpy
from flask import Flask, jsonify
from flask.json import JSONEncoder

from salicml.middleware import Middleware


class CustomJSONEncoder(JSONEncoder):

    def default(self, obj):
        if isinstance(obj, numpy.bool_):
            return 'True' if obj else 'False'

        return super(CustomJSONEncoder, self).default(obj)


app = Flask(__name__)
app.json_encoder = CustomJSONEncoder

middleware = Middleware()
middleware.train_all()


@app.route('/metric/number_of_itens/<int:pronac>', methods=['GET'])
def get_metric_number_of_items(pronac):
    result = middleware.get_metric_number_of_items(pronac)
    return jsonify(result), 200


if __name__ == '__main__':
    app.run(debug = True)
