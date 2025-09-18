from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import routes.todo as todo_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(todo_router.router, prefix="/", tags=["index"])
