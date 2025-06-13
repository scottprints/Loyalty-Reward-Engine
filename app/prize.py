from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Customer, Prize, PointsTransaction
from app import db

prize_bp = Blueprint('prize', __name__, url_prefix='/api')

@prize_bp.route('/prizes', methods=['GET'])
def list_prizes():
    prizes = Prize.query.filter_by(is_active=True).all()
    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "pointCost": p.point_cost,
            "weight": p.weight,
            "isActive": p.is_active
        } for p in prizes
    ])

@prize_bp.route('/redeem/<int:prize_id>', methods=['POST'])
@jwt_required()
def redeem_prize(prize_id):
    user_id = get_jwt_identity()
    customer = Customer.query.filter_by(id=user_id).first()
    if not customer:
        return jsonify({"error": "Customer not found."}), 404

    prize = Prize.query.filter_by(id=prize_id, is_active=True).first()
    if not prize:
        return jsonify({"error": "Prize not found or inactive."}), 404

    if customer.points < prize.point_cost:
        return jsonify({"error": "Not enough points to redeem this prize."}), 400

    customer.points -= prize.point_cost
    db.session.add(PointsTransaction(
        customer=customer,
        amount=-prize.point_cost,
        reason=f"Redeemed prize: {prize.name}"
    ))
    db.session.commit()

    return jsonify({
        "message": f"Redeemed {prize.name}",
        "points": customer.points
    }), 200 