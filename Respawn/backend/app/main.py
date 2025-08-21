from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import create_tables
from .routers import users, quests, bosses

# Create FastAPI app
app = FastAPI(
    title="Respawn API",
    description="Quit Addictions RPG Tracker - MVP Foundation",
    version="0.1.0"
)

# Add CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],  # Frontend dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router)
app.include_router(quests.router)
app.include_router(bosses.router)

@app.get("/")
async def root():
    """
    Root endpoint - API health check
    """
    return {"message": "Respawn API running"}

@app.on_event("startup")
async def startup_event():
    """
    Create database tables on startup if they don't exist
    """
    create_tables()
    print("Database tables created/verified")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
