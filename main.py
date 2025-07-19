from fastapi import FastAPI

app = FastAPI(
    title="OMNIMIND",
    description="The Autonomous, Self-Simulating, Self-Evolving Cognitive Kernel",
    version="0.1.0"
)

@app.get("/")
def read_root():
    return {"message": "👋 Welcome to OMNIMIND — The Autonomous, Self-Evolving Cognitive Kernel."}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "OMNIMIND"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 