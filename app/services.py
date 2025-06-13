import random
from datetime import datetime, timedelta, timezone

SPIN_LIMIT_PER_HOUR = 5


def get_spins_in_last_hour(customer) -> int:
    from app.models import SpinResult
    one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)
    return SpinResult.query.filter(
        SpinResult.customer_id == customer.id,
        SpinResult.spun_at >= one_hour_ago
    ).count()

def weighted_random_choice(prizes):
    weights = [p.weight for p in prizes]
    return random.choices(prizes, weights=weights, k=1)[0]

def spin_wheel(customer) -> dict:
    from app.models import Prize, PointsTransaction, SpinResult
    from app import db
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

    # Award points if this prize gives points
    if getattr(prize, 'points_award', 0) > 0:
        customer.points += prize.points_award
        db.session.add(PointsTransaction(
            customer=customer,
            amount=prize.points_award,
            reason=f"Prize: {prize.name}"
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