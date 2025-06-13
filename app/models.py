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

    spin_results = relationship('SpinResult', back_populates='customer', cascade='all, delete-orphan')
    points_transactions = relationship('PointsTransaction', back_populates='customer', cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f'<Customer {self.email}>' 