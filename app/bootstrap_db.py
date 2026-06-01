from __future__ import annotations

from .db import engine
from .models import Base


def main() -> None:
    Base.metadata.create_all(bind=engine)
    print("✅ Databastabeller skapade (om de inte fanns).")


if __name__ == "__main__":
    main()