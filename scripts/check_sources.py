from app.db import SessionLocal
from app.models import EmissionFactor

db = SessionLocal()

try:
    factors = db.query(EmissionFactor).limit(5).all()
    for f in factors:
        print(f"{f.category}/{f.key} source={f.source}")
finally:
    db.close()