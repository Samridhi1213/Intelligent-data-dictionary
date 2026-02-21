from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import schema_router, chat_router
from backend.config import settings

app = FastAPI(title="Intelligent Data Dictionary API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(schema_router.router, prefix="/api/schema", tags=["schema"])
app.include_router(chat_router.router, prefix="/api/chat", tags=["chat"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Intelligent Data Dictionary API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
