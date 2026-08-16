from fastapi import FastAPI

from src.routers import messages, users


app = FastAPI(
    title="Messenger API",
    version="0.1.0",
)


app.include_router(users.router)
app.include_router(messages.router)


@app.get("/")
def root():
    return {"message": "Messenger API is running"}
