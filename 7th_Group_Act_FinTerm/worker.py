from supabase import create_client
from datetime import datetime, timezone
import os
import time
from dotenv import load_dotenv

load_dotenv()

# Initialize Supabase client
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

# Step 2: Throughput counter -- tracks how many votes the worker has processed
votes_processed = 0

def process_votes():
    """
    Polls vote_queue for unprocessed votes (like Pub/Sub pull subscription).
    Handles decoding, deduplication, storage, and acknowledgment.
    """
    global votes_processed

    result = supabase.table("vote_queue") \
        .select("*") \
        .eq("processed", False) \
        .limit(10) \
        .execute()

    for vote in result.data:
        try:
            # Step 1: Log when the worker receives the vote (for latency measurement)
            received_at = time.time()
            print(f"[RECEIVED] User: {vote['user_id']} | Time: {received_at}")

            # Step 2: Idempotency key -- same as Firestore doc_id
            # Ensures duplicate messages result in the same final state
            doc_id = f"{vote['user_id']}_{vote['poll_id']}"

            # Step 3: Check if this vote already exists (duplicate detection)
            existing = supabase.table("votes") \
                .select("doc_id") \
                .eq("doc_id", doc_id) \
                .execute()

            if existing.data:
                print(f"[DUPLICATE DETECTED] doc_id: {doc_id} already exists -- skipping duplicate write")

            # Convert float timestamp to ISO format for Supabase compatibility
            processed_at_iso = datetime.fromtimestamp(received_at, tz=timezone.utc).isoformat()

            # Upsert into final votes table (idempotent write)
            # If the same vote arrives twice, it just overwrites the same record
            supabase.table("votes").upsert({
                "doc_id": doc_id,
                "user_id": vote["user_id"],
                "poll_id": vote["poll_id"],
                "choice": vote["choice"],
                "timestamp": vote["timestamp"],
                "edge_id": vote.get("edge_id"),
                "processed_at": processed_at_iso
            }).execute()

            # Mark as processed (equivalent to message.ack())
            # Tells the system this vote has been successfully handled
            supabase.table("vote_queue") \
                .update({"processed": True}) \
                .eq("id", vote["id"]) \
                .execute()

            # Step 1: End-to-end latency measurement
            # Compares vote creation time at edge vs processing time at worker
            latency = received_at - vote["timestamp"]
            print(f"[LATENCY] {latency:.2f}s for User: {vote['user_id']}")

            # Step 2: Throughput counter
            votes_processed += 1
            print(f"[PROCESSED] User: {vote['user_id']} | Poll: {vote['poll_id']} | Total Processed: {votes_processed}")

        except Exception as e:
            # Not marking as processed = automatic retry (like message.nack())
            # The worker will retry this vote on the next poll cycle
            print(f"[ERROR] Failed to process {vote['id']}: {e}")

def check_consistency():
    """
    Step 4: Evaluating consistency across components.
    Compares total counts across vote_queue and votes table.
    Prints automatically every 10 cycles.
    """
    total_received = supabase.table("vote_queue").select("id", count="exact").execute()
    total_processed = supabase.table("vote_queue").select("id", count="exact").eq("processed", True).execute()
    total_stored = supabase.table("votes").select("doc_id", count="exact").execute()

    print("\n===== CONSISTENCY CHECK =====")
    print(f"Total received (vote_queue):  {total_received.count}")
    print(f"Total processed (vote_queue): {total_processed.count}")
    print(f"Total stored (votes):         {total_stored.count}")
    print("=============================\n")

def run_worker():
    """
    Continuous processing loop.
    Listens for new votes without manual intervention,
    reflecting real-world event-driven distributed systems.
    """
    print("Worker service starting, listening for votes...")
    cycle = 0
    while True:
        process_votes()
        cycle += 1

        # Step 4: Print consistency check every 10 cycles
        if cycle % 10 == 0:
            check_consistency()

        time.sleep(2)  # poll every 2 seconds

if __name__ == "__main__":
    run_worker()