from app.routes.question_routes import router as question_router
from app.routes.test_routes import router as test_router
from fastapi.middleware.cors import CORSMiddleware
from app.routes.auth_routes import auth_router
from fastapi import FastAPI
import os, uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(test_router)
app.include_router(question_router)

SECRET_KEY = os.getenv('SECRET_KEY')

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY environment not found")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)