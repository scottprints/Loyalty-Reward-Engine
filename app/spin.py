from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Customer
from app.services import spin_wheel
from app import db

spin_bp = Blueprint('spin', __name__, url_prefix='/api')

@spin_bp.route('/spin', methods=['POST'])
@jwt_required()
def spin():
    user_id = get_jwt_identity()
    customer = Customer.query.filter_by(id=user_id).first()
    if not customer:
        return jsonify({"error": "Customer not found."}), 404

    result = spin_wheel(customer)
    if "error" in result:
        # 429 for rate limit, 400 for other errors
        if "limit" in result["error"].lower():
            return jsonify(result), 429
        return jsonify(result), 400
    return jsonify(result), 200 