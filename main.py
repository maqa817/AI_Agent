from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from freshguard_ai import analyze_retail_data

app = FastAPI(title="FreshGuard AI Backend")

# Allow CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Endpoint to receive data and return AI analysis
@app.post("/api/analyze")
async def analyze_data(request: Request):
    try:
        data = await request.json()
        print("Received payload for analysis.")
        
        result = analyze_retail_data(data)
        
        if isinstance(result, dict) and "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
            
        return result
    except Exception as e:
        print(f"Error during analysis: {e}")
        raise HTTPException(status_code=400, detail=str(e))

# Mount the static directory for the frontend
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    print("Starting FreshGuard Backend Server on http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)
