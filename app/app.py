from flask import Flask, Blueprint
from flask_restful import Api, Resource, url_for

from resources.StockPrice import StockPrice

app = Flask(__name__)
api_bp = Blueprint('api', __name__)
api = Api(api_bp)

api.add_resource(StockPrice, '/stockprice/', '/')

app.register_blueprint(api_bp)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

