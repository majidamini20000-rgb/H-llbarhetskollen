from __future__ import annotations

import datetime as dt

from fastapi import Depends, FastAPI, HTTPException, Query, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import Base, get_session, engine
from app.models import Activity, EmissionFactor, User
from app.schemas import (
    ActivityCreate,
    ActivityOut,
    EmissionFactorOut,
    UserCreate,
    UserOut,
    WeeklyReportOut,
)
from app.services.emissions import Factor, FactorMap, calculate_co2e

app = FastAPI(title="Hållbarhetskollen API (starter)")

from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="static"), name="static")

Base.metadata.create_all(bind=engine)



db = Session(bind=engine)

if not db.query(EmissionFactor).first():

    factors = [
        EmissionFactor(
            category="travel",
            key="car",
            unit="km",
            co2e_per_unit=0.2,
            source="default",
            scope="transport"
        ),
        EmissionFactor(
            category="travel",
            key="bus",
            unit="km",
            co2e_per_unit=0.08,
            source="default",
            scope="transport"
        ),
        EmissionFactor(
            category="food",
            key="meat",
            unit="portion",
            co2e_per_unit=2.5,
            source="default",
            scope="food"
        ),
        EmissionFactor(
            category="energy",
            key="electricity",
            unit="kwh",
            co2e_per_unit=0.05,
            source="default",
            scope="energy"
        ),
    ]

    db.add_all(factors)
    db.commit()

db.close()

 
templates = Jinja2Templates(directory="templates")




@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/users", response_model=UserOut)
def create_user(payload: UserCreate, db: Session = Depends(get_session)) -> User:
    user = User(name=payload.name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.get("/users", response_model=list[UserOut])
def list_users(db: Session = Depends(get_session)) -> list[User]:
    return list(db.execute(select(User)).scalars().all())


def _load_factor_map(db: Session) -> FactorMap:
    factors = db.execute(select(EmissionFactor)).scalars().all()
    mapping: FactorMap = {}
    for f in factors:
        mapping[(f.category, f.key)] = Factor(
            category=f.category,
            key=f.key,
            unit=f.unit,
            co2e_per_unit=f.co2e_per_unit,
        )
    return mapping


@app.get("/emission-factors", response_model=list[EmissionFactorOut])
def list_factors(db: Session = Depends(get_session)) -> list[EmissionFactor]:
    return list(db.execute(select(EmissionFactor)).scalars().all())


@app.post("/activities", response_model=ActivityOut)
def create_activity(payload: ActivityCreate, db: Session = Depends(get_session)) -> ActivityOut:
    user = db.get(User, payload.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    activity = Activity(
        user_id=payload.user_id,
        category=payload.category,
        key=payload.key,
        amount=payload.amount,
        date=payload.date,
    )
    db.add(activity)
    db.commit()
    db.refresh(activity)

    factors = _load_factor_map(db)
    try:
        co2e = calculate_co2e(activity.category, activity.key, activity.amount, factors)
    except KeyError:
        co2e = None

    return ActivityOut(
        id=activity.id,
        user_id=activity.user_id,
        category=activity.category,
        key=activity.key,
        amount=activity.amount,
        date=activity.date,
        co2e=co2e,
    )


@app.get("/activities", response_model=list[ActivityOut])
def list_activities(
    user_id: int | None = Query(default=None),
    db: Session = Depends(get_session),
) -> list[ActivityOut]:

    stmt = select(Activity)
    if user_id is not None:
        stmt = stmt.where(Activity.user_id == user_id)

    activities = list(db.execute(stmt).scalars().all())
    factors = _load_factor_map(db)

    out: list[ActivityOut] = []
    for a in activities:
        try:
            co2e = calculate_co2e(a.category, a.key, a.amount, factors)
        except KeyError:
            co2e = None

        out.append(
            ActivityOut(
                id=a.id,
                user_id=a.user_id,
                category=a.category,
                key=a.key,
                amount=a.amount,
                date=a.date,
                co2e=co2e,
            )
        )

    return out


def _week_bounds(week_start: dt.date) -> tuple[dt.date, dt.date]:
    return week_start, week_start + dt.timedelta(days=6)


@app.get("/reports/weekly", response_model=WeeklyReportOut)
def weekly_report(
    user_id: int = Query(...),
    week_start: dt.date = Query(...),
    db: Session = Depends(get_session),
) -> WeeklyReportOut:

    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    start, end = _week_bounds(week_start)

    stmt = (
        select(Activity)
        .where(Activity.user_id == user_id)
        .where(Activity.date >= start)
        .where(Activity.date <= end)
    )

    activities = list(db.execute(stmt).scalars().all())
    factors = _load_factor_map(db)

    total = 0.0
    for a in activities:
        try:
            total += calculate_co2e(a.category, a.key, a.amount, factors)
        except KeyError:
            continue

    return WeeklyReportOut(
        user_id=user_id,
        week_start=start,
        week_end=end,
        total_co2e=total,
    )





@app.get("/ui", response_class=HTMLResponse)
def ui_home(request: Request):
    tpl = templates.get_template("index.html")
    html = tpl.render({"request": request})
    return HTMLResponse(html)



@app.get("/ui/users", response_class=HTMLResponse)
def ui_users(request: Request, db: Session = Depends(get_session)):

    users = db.execute(select(User).order_by(User.id.asc())).scalars().all()

    tpl = templates.get_template("create_user.html")

    html = tpl.render({
        "request": request,
        "users": users,
        "message": None,
        "error": None
    })

    return HTMLResponse(html)



@app.post("/ui/users", response_class=HTMLResponse)
def ui_create_user(
    request: Request,
    name: str = Form(...),
    db: Session = Depends(get_session)
):

    name = name.strip()

    tpl = templates.get_template("create_user.html")

    users = db.execute(select(User).order_by(User.id.asc())).scalars().all()

    if not name:
        html = tpl.render({
            "request": request,
            "users": users,
            "message": None,
            "error": "Name får inte vara tomt."
        })
        return HTMLResponse(html)

    user = User(name=name)
    db.add(user)
    db.commit()

    users = db.execute(select(User).order_by(User.id.asc())).scalars().all()

    html = tpl.render({
        "request": request,
        "users": users,
        "message": f"Skapade användare '{user.name}'",
        "error": None
    })

    return HTMLResponse(html)



@app.post("/ui/users/{user_id}/delete", response_class=HTMLResponse)
def ui_delete_user(
    user_id: int,
    request: Request,
    db: Session = Depends(get_session)
):

    tpl = templates.get_template("create_user.html")

    user = db.get(User, user_id)

    users = db.execute(select(User).order_by(User.id.asc())).scalars().all()

    if not user:
        html = tpl.render({
            "request": request,
            "users": users,
            "message": None,
            "error": f"Användare {user_id} finns inte"
        })
        return HTMLResponse(html)

    deleted_name = user.name

    db.delete(user)
    db.commit()

    users = db.execute(select(User).order_by(User.id.asc())).scalars().all()

    html = tpl.render({
        "request": request,
        "users": users,
        "message": f"Raderade användare '{deleted_name}'",
        "error": None
    })

    return HTMLResponse(html)

@app.get("/ui/activities", response_class=HTMLResponse)
def ui_activities(request: Request, db: Session = Depends(get_session)):

    users = db.execute(select(User).order_by(User.id.asc())).scalars().all()
    factors = db.execute(select(EmissionFactor).order_by(EmissionFactor.category)).scalars().all()

    db_activities = db.execute(
        select(Activity).order_by(Activity.id.desc())
    ).scalars().all()

    factor_map = _load_factor_map(db)

    activities = []
    for a in db_activities:
        try:
            co2e = calculate_co2e(a.category, a.key, a.amount, factor_map)
        except KeyError:
            co2e = None

        activities.append({
            "id": a.id,
            "user_id": a.user_id,
            "category": a.category,
            "key": a.key,
            "amount": a.amount,
            "date": a.date,
            "co2e": co2e
        })

    tpl = templates.get_template("activities.html")

    return HTMLResponse(tpl.render({
        "request": request,
        "users": users,
        "activities": activities,
        "factors": factors,
        "message": None,
        "error": None
    }))

@app.post("/ui/activities", response_class=HTMLResponse)
def ui_create_activity(
    request: Request,
    user_id: int = Form(...),
    category: str = Form(...),
    key: str = Form(...),
    amount: float = Form(...),
    date: str = Form(...),
    db: Session = Depends(get_session),
):

    tpl = templates.get_template("activities.html")

    users = db.execute(select(User).order_by(User.id.asc())).scalars().all()
    factors = db.execute(select(EmissionFactor).order_by(EmissionFactor.category)).scalars().all()

    try:
        parsed_date = dt.date.fromisoformat(date)
    except ValueError:
        activities = db.execute(select(Activity).order_by(Activity.id.desc())).scalars().all()
        return HTMLResponse(tpl.render({
            "request": request,
            "users": users,
            "activities": activities,
            "factors": factors,
            "message": None,
            "error": "Fel datumformat"
        }))

   
    if amount <= 0:
        activities = db.execute(select(Activity).order_by(Activity.id.desc())).scalars().all()
        return HTMLResponse(tpl.render({
            "request": request,
            "users": users,
            "activities": activities,
            "factors": factors,
            "message": None,
            "error": "Amount måste vara större än 0"
        }))

  
    user = db.get(User, user_id)
    if not user:
        activities = db.execute(select(Activity).order_by(Activity.id.desc())).scalars().all()
        return HTMLResponse(tpl.render({
            "request": request,
            "users": users,
            "activities": activities,
            "factors": factors,
            "message": None,
            "error": "Användaren finns inte"
        }))

    activity = Activity(
        user_id=user_id,
        category=category,
        key=key,
        amount=amount,
        date=parsed_date,
    )

    db.add(activity)
    db.commit()

    activities_db = db.execute(
        select(Activity).order_by(Activity.id.desc())
    ).scalars().all()


    factor_map = _load_factor_map(db)

    activities = []
    for a in activities_db:
        try:
            co2e = calculate_co2e(a.category, a.key, a.amount, factor_map)
        except KeyError:
            co2e = None

        activities.append({
            "id": a.id,
            "user_id": a.user_id,
            "category": a.category,
            "key": a.key,
            "amount": a.amount,
            "date": a.date,
            "co2e": co2e
        })

    return HTMLResponse(tpl.render({
        "request": request,
        "users": users,
        "activities": activities,
        "factors": factors,
        "message": "Aktivitet sparad!",
        "error": None
    }))

@app.get("/ui/reports/weekly", response_class=HTMLResponse)
def ui_weekly(
    request: Request,
    user_id: int | None = None,
    week_start: str | None = None,
    db: Session = Depends(get_session),
):

    users = db.execute(select(User)).scalars().all()
    tpl = templates.get_template("weekly.html")

    total = None
    week_end = None
    error = None
    activities = []

    if user_id is not None and week_start:
        try:
            start = dt.date.fromisoformat(week_start)

        except ValueError:
            error = "Fel datumformat"
            start = None
            end = None

        else:
         
            if start.weekday() != 0:
                error = "Datumet måste vara en måndag"
                start = None
                end = None
            else:
                end = start + dt.timedelta(days=6)

                stmt = (
                    select(Activity)
                    .where(Activity.user_id == user_id)
                    .where(Activity.date >= start)
                    .where(Activity.date <= end)
                )

                db_activities = db.execute(stmt).scalars().all()
                factors = _load_factor_map(db)

                activities = []
                total = 0.0

                for a in db_activities:
                    try:
                        co2e = calculate_co2e(
                            a.category,
                            a.key,
                            a.amount,
                            factors
                        )
                    except KeyError:
                        co2e = None

                    activities.append({
                        "category": a.category,
                        "key": a.key,
                        "amount": a.amount,
                        "date": a.date,
                        "co2e": co2e
                    })

                    if co2e is not None:
                        total += co2e

                week_end = end

    html = tpl.render({
        "request": request,
        "users": users,
        "total": total,
        "week_start": week_start,
        "week_end": week_end,
        "activities": activities,
        "error": error
    })

    return HTMLResponse(html)