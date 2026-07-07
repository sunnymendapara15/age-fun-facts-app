# Age Fun Facts App

A full-stack age calculator with fun, shareable facts built with React (Create React App) on the frontend and FastAPI on the backend.

## Features

- Enter your birthdate to see your age broken down into years, months, days, and total days lived.
- Enjoy playful fun facts generated from your age (leap years experienced, dog years, upcoming birthday countdown, lifetime milestones).
- Backend validates birthdates, guards against future dates, and exposes a single `/api/age` endpoint.
- Frontend communicates with the backend via a development proxy for seamless local development.

## Stack

| Layer    | Technology |
|----------|------------|
| Frontend | React (Create React App) |
| Backend  | FastAPI + Uvicorn |

## Getting started

### 1. Run the backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Use `.venv\Scripts\activate` on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The backend exposes the age calculator at `http://localhost:8000/api/age` and allows cross-origin requests from any origin for local development.

### 2. Run the frontend

```bash
cd frontend
npm install
npm start
```

Create React App will proxy `/api/age` requests to the backend automatically thanks to the `proxy` entry in `package.json`. The UI will be available at `http://localhost:3000`.

## Testing the calculator

1. Open [http://localhost:3000](http://localhost:3000) in your browser.
2. Enter a birthdate using the picker and click "Calculate Age".
3. Review the age breakdown and fun facts returned from the backend. Invalid dates or future dates will surface a friendly error.

## Future improvements

- Add optional time-of-day inputs for more precise age calculations.
- Persist favorite fun facts for sharing or daily notifications.
- Add age-based milestones (e.g., powered by public APIs for historical events in the birth year).
