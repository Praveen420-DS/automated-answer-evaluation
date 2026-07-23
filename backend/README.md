# AASE Backend

Flask API scaffold for Automated Answer Script Evaluation.

```bash
cd backend
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
python app.py
```

For a complete local stack, copy `backend/.env.example` to `backend/.env`, set
strong secrets, then run `docker compose up --build`. MongoDB is exposed on
`localhost:27017` and the API on `localhost:5000`.

The health endpoint is available at `GET /api/health`.
