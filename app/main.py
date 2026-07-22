from fastapi import FastAPI

from app.api.routes import router


app = FastAPI(
    title="Automated Answer Script Evaluation API",
    description="Backend API for automated answer sheet processing",
    version="1.0.0"
)


app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "Automated Answer Evaluation API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }