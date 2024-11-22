from app.routes.question_routes import router as question_router
from app.routes.test_routes import router as test_router
from fastapi.middleware.cors import CORSMiddleware
from app.routes.auth_routes import auth_router
from app.sevices import jwt_service
from fastapi import FastAPI
import uvicorn

jwt_service.validate_settings()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(test_router)
app.include_router(question_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)