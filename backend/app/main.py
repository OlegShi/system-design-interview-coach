from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.sessions import router as sessions_router

app = FastAPI(title="System Design Interview Coach")

# Allow Next.js dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sessions_router)

@app.get("/health")
def health():
    return {"status": "ok"}
