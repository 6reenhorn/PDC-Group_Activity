from supabase import create_client
import os
import time
from dotenv import load_dotenv

load_dotenv()

# Initialize Supabase client
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

def process_votes():
    """
    Step 1: Poll vote_queue for unprocessed votes (like Pub/Sub pull subscription).
    Decodes, validates, deduplicates, and stores each vote.
    """
    result = supabase.table("vote_queue") \
        .select("*") \
        .eq("processed", False) \
        .limit(10) \
        .execute()

    for vote in result.data:
        try:
            # Step 2: Idempotency key -- same as Firestore doc_id
            # Ensures duplicate messages result in the same final state
            doc_id = f"{vote['user_id']}_{vote['poll_id']}"

            # Step 3: Upsert into final votes table (idempotent write)
            # If the same vote arrives twice, it just overwrites the same record
            supabase.table("votes").upsert({
                "doc_id": doc_id,
                "user_id": vote["user_id"],
                "poll_id": vote["poll_id"],
                "choice": vote["choice"],
                "timestamp": vote["timestamp"],
                "edge_id": vote.get("edge_id"),
                "processed_at": time.time()  # track when it was processed
            }).execute()

            # Step 4: Mark as processed (equivalent to message.ack())
            # Tells the system this vote has been successfully handled
            supabase.table("vote_queue") \
                .update({"processed": True}) \
                .eq("id", vote["id"]) \
                .execute()

            # Track end-to-end latency
            latency = time.time() - vote["timestamp"]
            print(f"[PROCESSED] User: {vote['user_id']} | Poll: {vote['poll_id']} | Latency: {latency:.2f}s")

        except Exception as e:
            # Step 4: Not marking as processed = automatic retry (like message.nack())
            # The worker will retry this vote on the next poll cycle
            print(f"[ERROR] Failed to process {vote['id']}: {e}")

def run_worker():
    """
    Step 5: Continuous processing loop.
    Listens for new votes without manual intervention,
    reflecting real-world event-driven distributed systems.
    """
    print("Worker service starting, listening for votes...")
    while True:
        process_votes()
        time.sleep(2)  # poll every 2 seconds

if __name__ == "__main__":
    run_worker()