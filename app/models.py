import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy import func
from app import db

class Customer(db.Model):
    __tablename__ = 'customer'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    points = db.Column(db.Integer, nullable=False, default=0)
    password_hash = db.Column(db.String(255), nullable=True)

    spin_results = relationship('SpinResult', back_populates='customer', cascade='all, delete-orphan')
    points_transactions = relationship('PointsTransaction', back_populates='customer', cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f'<Customer {self.email}>'

class Prize(db.Model):
    __tablename__ = 'prize'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    point_cost = db.Column(db.Integer, nullable=False, default=0)
    weight = db.Column(db.Integer, nullable=False, default=1)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    points_award = db.Column(db.Integer, nullable=False, default=0)

    spin_results = relationship('SpinResult', back_populates='prize', cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f'<Prize {self.name}>'

class SpinResult(db.Model):
    __tablename__ = 'spin_result'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.ForeignKey('customer.id'), nullable=False)
    prize_id = db.Column(db.ForeignKey('prize.id'), nullable=False)
    spun_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)

    customer = relationship('Customer', back_populates='spin_results')
    prize = relationship('Prize', back_populates='spin_results')

    def __repr__(self) -> str:
        return f'<SpinResult customer={self.customer_id} prize={self.prize_id}>'

class PointsTransaction(db.Model):
    __tablename__ = 'points_transaction'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.ForeignKey('customer.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)

    customer = relationship('Customer', back_populates='points_transactions')

    def __repr__(self) -> str:
        return f'<PointsTransaction customer={self.customer_id} amount={self.amount}>' 