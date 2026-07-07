from datetime import date, datetime
from typing import List

from dateutil.relativedelta import relativedelta
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="Age Fun Facts API",
    description="Calculate a precise age breakdown and batch of fun facts for a given birthdate.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AgeRequest(BaseModel):
    birthdate: date = Field(..., description="Birthdate in YYYY-MM-DD format")


class AgeResponse(BaseModel):
    years: int
    months: int
    days: int
    total_days: int
    fun_facts: List[str]


def is_leap_year(year: int) -> bool:
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


def leap_years_between(start: date, end: date) -> int:
    leaps = 0
    for year in range(start.year, end.year + 1):
        if not is_leap_year(year):
            continue
        leap_day = date(year, 2, 29)
        if start <= leap_day <= end:
            leaps += 1
    return leaps


def next_leap_birthday(reference: date, birth: date) -> date:
    year = reference.year if (reference.month, reference.day) < (birth.month, birth.day) else reference.year + 1
    candidate_year = year
    while True:
        try:
            return date(candidate_year, birth.month, birth.day)
        except ValueError:
            # Handles February 29 on non-leap year: skip until we find a leap year
            candidate_year += 1


@app.post("/api/age", response_model=AgeResponse)
def calculate_age(payload: AgeRequest) -> AgeResponse:
    today = datetime.utcnow().date()
    if payload.birthdate > today:
        raise HTTPException(status_code=400, detail="Birthdate cannot be in the future.")

    reference_datetime = datetime.combine(payload.birthdate, datetime.min.time())
    now_datetime = datetime.utcnow()
    delta = relativedelta(now_datetime, reference_datetime)

    total_days = (now_datetime.date() - payload.birthdate).days

    leaps = leap_years_between(payload.birthdate, now_datetime.date())
    next_birthday_date = next_leap_birthday(now_datetime.date(), payload.birthdate)
    days_until_next_birthday = (next_birthday_date - now_datetime.date()).days

    fun_facts = [
        f"You have celebrated {delta.years} birthdays (the math says you're {delta.years} years old!).",
        f"Leap years lived through: {leaps}.",
        f"In dog years you are approximately {delta.years * 7} years old.",
        f"Roughly {total_days // 7} weeks have passed since your birthday.",
        f"About {total_days // 29} full moons have risen since you were born.",
    ]

    if days_until_next_birthday == 0:
        fun_facts.append("Happy birthday! Today is your special day 🎉 .")
    else:
        fun_facts.append(f"Your next birthday lands in {days_until_next_birthday} day(s).")

    fun_facts.append(f"You've lived the equivalent of {total_days // 365} full solar years worth of days.")

    return AgeResponse(
        years=delta.years,
        months=delta.months,
        days=delta.days,
        total_days=total_days,
        fun_facts=fun_facts,
    )
