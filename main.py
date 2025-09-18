from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import routes.todo as todo_router

app = FastAPI()

# allow only your frontend origin (HTTPS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://mixed-app-1022365474768.southamerica-east1.run.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "API is running"}

app.include_router(todo_router.router, prefix="/todos", tags=["todos"])
