from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.chat_router import router as chat_router
from routers.sentiment_router import router as sentiment_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow this origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include routers
app.include_router(chat_router, prefix="/api")
app.include_router(sentiment_router, prefix="/api")


@app.get("/")
def read_root():
    return {"Hello": "World"}
