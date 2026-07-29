# Executive Search Platform

A multi-step executive search platform built with FastAPI.

## Project Structure

```
/backend/          Backend API (FastAPI)
  /app/
    /step1/        Candidate sourcing and profiling
    /step2/        Assessment and evaluation
    /step3/        Client matching and shortlisting
    /step4/        Offer management and onboarding
/frontend/         Frontend application
/docs/             Project documentation
/scripts/          Utility scripts
```

## Getting Started

```bash
# Install dependencies
pip install -r backend/requirements.txt

# Run the server
uvicorn app.main:app --reload --app-dir backend
```

## Environment Variables

Copy `.env.example` to `.env` and update the values.
