# Automated Answer Evaluation

An explainable, rubric-driven, human-in-the-loop AI system for automated answer script evaluation.

## Core Features

- Answer Script Upload
- OCR / Text Extraction
- Question Segmentation
- Rubric-Based Evaluation
- Concept Coverage
- Semantic Similarity
- Completeness Score
- Explainable Scoring
- AI Feedback
- Teacher Review and Override

## Team

- Member 1 – Frontend
- Member 2 – AI/ML
- Member 3 – Backend & Integration

## Architecture

Upload
↓
OCR
↓
Question Segmentation
↓
Evaluation Engine
↓
Explainable Score
↓
AI Feedback
↓
Teacher Review

## Getting Started

### Backend

1. Copy `backend/.env.example` to `backend/.env` and update values as needed.
2. Create and activate a virtual environment:

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
```

3. Install backend dependencies:

```bash
pip install -r requirements.txt
```

4. Start the API server:

```bash
python app.py
```

The backend health endpoint is available at `http://localhost:5000/api/health`.

### Frontend

1. Install frontend dependencies:

```bash
cd frontend
npm install
```

2. Run the frontend:

```bash
npm run dev
```

### Local Docker Stack

A complete local stack is available via Docker Compose. From the repository root:

```bash
docker compose up --build
```

This starts MongoDB and the backend API.

### Tests

Run backend tests from the repository root using the backend virtual environment:

```bash
cd backend
.venv\Scripts\python.exe -m pytest -q tests
```
