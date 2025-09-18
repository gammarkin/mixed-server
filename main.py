from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import routes.todo as todo_router

app = FastAPI()

@app.middleware("http")
async def enforce_https(request: Request, call_next):
    if request.url.scheme == "http":
        url = request.url.replace(scheme="https")
        return RedirectResponse(url)
    return await call_next(request)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "API is running"}

app.include_router(todo_router.router, prefix="/todos", tags=["todos"])
