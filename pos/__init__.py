from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('config.Config')
app.url_map.strict_slashes = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from pos.routes.items import items_bp
from pos.routes.orders import orders_bp

app.register_blueprint(items_bp, url_prefix="/api/v1/items")
app.register_blueprint(orders_bp, url_prefix="/api/v1/orders")


# Error handlers
@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': str(error)}), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': str(error)}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': str(error)}), 500
