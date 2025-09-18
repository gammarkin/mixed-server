from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import routes.todo as todo_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://mixed-app-1022365474768.southamerica-east1.run.app",   
        "http://localhost:8080",
        "http://localhost:19006",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "API is running"}

app.include_router(todo_router.router, prefix="/todos", tags=["todos"])
