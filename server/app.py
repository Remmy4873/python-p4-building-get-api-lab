#!/usr/bin/env python3

import logging
from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>', 200

# GET /bakeries: returns a list of JSON objects for all bakeries in the database.
@app.route('/bakeries', methods=['GET'])
def get_bakeries():
    try:
        bakeries = Bakery.query.all()
        bakeries_json = [bakery.to_dict() for bakery in bakeries]
        return make_response(jsonify(bakeries_json), 200)
    except Exception as e:
        logger.error(f"Error fetching bakeries: {e}")
        return make_response(jsonify({"error": str(e)}), 500)

# GET /bakeries/<int:id>: returns a single bakery as JSON with its baked goods nested in a list.
@app.route('/bakeries/<int:id>', methods=['GET'])
def get_bakery_by_id(id):
    try:
        bakery = Bakery.query.filter_by(id=id).first()
        if bakery:
            bakery_json = bakery.to_dict(nested=True)
            return make_response(jsonify(bakery_json), 200)
        else:
            logger.warning(f"Bakery with id {id} not found.")
            return make_response(jsonify({"error": "Bakery not found"}), 404)
    except Exception as e:
        logger.error(f"Error fetching bakery by id {id}: {e}")
        return make_response(jsonify({"error": str(e)}), 500)

# GET /baked_goods/by_price: returns a list of baked goods as JSON, sorted by price in descending order.
@app.route('/baked_goods/by_price', methods=['GET'])
def get_baked_goods_by_price():
    try:
        baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
        baked_goods_json = [baked_good.to_dict() for baked_good in baked_goods]
        return make_response(jsonify(baked_goods_json), 200)
    except Exception as e:
        logger.error(f"Error fetching baked goods by price: {e}")
        return make_response(jsonify({"error": str(e)}), 500)

# GET /baked_goods/most_expensive: returns the single most expensive baked good as JSON.
@app.route('/baked_goods/most_expensive', methods=['GET'])
def get_most_expensive_baked_good():
    try:
        most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).first()
        if most_expensive:
            baked_good_json = most_expensive.to_dict()
            return make_response(jsonify(baked_good_json), 200)
        else:
            logger.warning("No baked goods found.")
            return make_response(jsonify({"error": "No baked goods found"}), 404)
    except Exception as e:
        logger.error(f"Error fetching most expensive baked good: {e}")
        return make_response(jsonify({"error": str(e)}), 500)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
