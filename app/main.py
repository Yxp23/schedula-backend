from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Schedula API")

# Enable CORS so frontend can talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Schedula API is running! 🎓"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/api/courses")
def get_courses():
    # We'll implement this later
    return {"courses": []}