import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import csv
from app import create_app, db
from app.models import Prize

app = create_app()
with app.app_context():
    with open('prizes_backup.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            prize = Prize(
                name=row['Name'],
                point_cost=int(row['Point Cost']),
                weight=int(row['Weight']),
                is_active=row['Is Active'].strip().lower() in ('true', '1', 'yes'),
                points_award=int(row['Points Award'])
            )
            db.session.add(prize)
        db.session.commit()
    print("Prizes imported successfully.")