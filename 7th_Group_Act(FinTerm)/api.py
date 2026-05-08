from fastapi import FastAPI, HTTPException
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Initialize Supabase client
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

@app.post("/vote")
def receive_vote(vote: dict):
    """
    Receives vote from edge nodes, validates it,
    and inserts it into vote_queue (acts as Pub/Sub publish).
    """
    # Step 1: Validate required fields
    required = ["user_id", "poll_id", "choice"]
    if not all(k in vote for k in required):
        raise HTTPException(status_code=400, detail="Missing required fields")

    try:
        # Step 2: Insert into vote_queue (equivalent to publishing to Pub/Sub)
        # This enables asynchronous processing by the worker
        supabase.table("vote_queue").insert({
            "user_id": vote["user_id"],
            "poll_id": vote["poll_id"],
            "choice": vote["choice"],
            "timestamp": vote["timestamp"],
            "edge_id": vote.get("edge_id", "unknown"),
            "processed": False  # worker will mark this True after processing
        }).execute()

        print(f"[ACCEPTED] User: {vote['user_id']} | Choice: {vote['choice']} | Edge: {vote.get('edge_id', 'unknown')}")
        return {"status": "accepted"}

    except Exception as e:
        print(f"[ERROR] Failed to queue vote: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def health_check():
    """Health check endpoint to verify API is running."""
    return {"status": "API is running"}