from fastapi import FastAPI
from routers.chat_router import router as chat_router

app = FastAPI()

# Include routers
app.include_router(chat_router, prefix="/api")

@app.get("/")
def read_root():
    return {"Hello": "World"}
