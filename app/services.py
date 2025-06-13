import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models import Customer, Prize, SpinResult, PointsTransaction
from app import db

SPIN_LIMIT_PER_HOUR = 5


def get_spins_in_last_hour(customer: Customer) -> int:
    one_hour_ago = datetime.now(datetime.UTC) - timedelta(hours=1)
    return SpinResult.query.filter(
        SpinResult.customer_id == customer.id,
        SpinResult.spun_at >= one_hour_ago
    ).count()

def weighted_random_choice(prizes: list[Prize]) -> Prize:
    weights = [p.weight for p in prizes]
    return random.choices(prizes, weights=weights, k=1)[0]

def spin_wheel(customer: Customer) -> dict:
    if get_spins_in_last_hour(customer) >= SPIN_LIMIT_PER_HOUR:
        return {"error": "Spin limit reached. Try again later."}

    prizes = Prize.query.filter_by(is_active=True).all()
    if not prizes:
        return {"error": "No active prizes available."}

    prize = weighted_random_choice(prizes)

    if prize.point_cost > 0 and customer.points < prize.point_cost:
        return {"error": "Not enough points to spin for this prize."}

    # Deduct points if needed
    if prize.point_cost > 0:
        customer.points -= prize.point_cost
        db.session.add(PointsTransaction(
            customer=customer,
            amount=-prize.point_cost,
            reason=f"Spin for prize: {prize.name}"
        ))

    # Log spin result
    spin_result = SpinResult(customer=customer, prize=prize)
    db.session.add(spin_result)
    db.session.commit()

    return {
        "prize": prize.name,
        "points": customer.points,
        "spinCountLastHour": get_spins_in_last_hour(customer),
        "spunAt": spin_result.spun_at.isoformat()
    } 