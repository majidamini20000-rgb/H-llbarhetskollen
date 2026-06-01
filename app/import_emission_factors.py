from __future__ import annotations

import csv
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from .db import SessionLocal
from .models import EmissionFactor


DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "emission_factors.csv"


def upsert_factor(db: Session, category: str, key: str, unit: str, co2e_per_unit: float, source: str | None) -> None:
    stmt = select(EmissionFactor).where(
        EmissionFactor.category == category,
        EmissionFactor.key == key,
        EmissionFactor.unit == unit,
    )
    existing = db.execute(stmt).scalar_one_or_none()
    if existing:
        existing.co2e_per_unit = co2e_per_unit
        existing.source = source
    else:
        db.add(
            EmissionFactor(
                category=category,
                key=key,
                unit=unit,
                co2e_per_unit=co2e_per_unit,
                source=source,
            )
        )


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Hittar inte: {DATA_PATH}")

    db = SessionLocal()
    try:
        with DATA_PATH.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                required = ["category", "key", "unit", "co2e_per_unit"]

                if any(not (row.get(k) or "").strip() for k in required):
                    print(f"[WARN] Skipping row: {row}")
                    continue
                category = row["category"].strip()
                key = row["key"].strip()
                unit = row["unit"].strip()
                co2e_per_unit = float(row["co2e_per_unit"])
                source = (row.get("source") or "").strip() or None
                upsert_factor(db, category, key, unit, co2e_per_unit, source)
                count += 1

        db.commit()
        print(f"✅ Import klar: {count} emissionsfaktorer.")
    finally:
        db.close()


if __name__ == "__main__":
    main()