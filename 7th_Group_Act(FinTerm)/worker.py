from supabase import create_client
import os, time
from dotenv import load_dotenv

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def process_votes():
    # Poll for unprocessed votes
    result = supabase.table("vote_queue") \
        .select("*") \
        .eq("processed", False) \
        .limit(10) \
        .execute()

    for vote in result.data:
        try:
            # Idempotency key (same as Firestore doc_id)
            doc_id = f"{vote['user_id']}_{vote['poll_id']}"

            # Upsert into final votes table
            supabase.table("votes").upsert({
                "doc_id": doc_id,
                "user_id": vote["user_id"],
                "poll_id": vote["poll_id"],
                "choice": vote["choice"],
                "timestamp": vote["timestamp"],
                "edge_id": vote.get("edge_id")
            }).execute()

            # Mark as processed
            supabase.table("vote_queue") \
                .update({"processed": True}) \
                .eq("id", vote["id"]) \
                .execute()

            print(f"[PROCESSED] {vote['user_id']} | Poll: {vote['poll_id']}")

        except Exception as e:
            # Not marking as processed = automatic retry
            print(f"[ERROR] Failed to process {vote['id']}: {e}")

def run_worker():
    print("Worker started...")
    while True:
        process_votes()
        time.sleep(2)

if __name__ == "__main__":
    run_worker()