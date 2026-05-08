from fastapi import FastAPI, HTTPException
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

@app.post("/vote")
def receive_vote(vote: dict):
    # Validate required fields
    required = ["user_id", "poll_id", "choice"]
    if not all(k in vote for k in required):
        raise HTTPException(status_code=400, detail="Missing required fields")

    try:
        # Insert into vote_queue
        supabase.table("vote_queue").insert({
            "user_id": vote["user_id"],
            "poll_id": vote["poll_id"],
            "choice": vote["choice"],
            "timestamp": vote["timestamp"],
            "edge_id": vote.get("edge_id", "unknown"),
            "processed": False
        }).execute()
        return {"status": "accepted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))