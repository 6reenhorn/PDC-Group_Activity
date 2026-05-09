import uuid
import random
import time
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Get API URL from .env file
API_URL = os.getenv("API_URL")

# Change this per group member (e.g., "node_john_cyril_espina")
EDGE_ID = "node_den_jester_antonio"

# Step 2: Throughput counter -- tracks how many votes this node has sent
votes_sent = 0

def generate_vote():
    """
    Generates a unique vote with an edge node identifier.
    Includes time_created for end-to-end latency measurement (Step 1).
    """
    now = time.time()
    return {
        "user_id": str(uuid.uuid4()),
        "poll_id": "poll_1",
        "choice": random.choice(["A", "B", "C"]),
        "timestamp": now,
        "time_created": now,    # Step 1: used for latency measurement at worker
        "edge_id": EDGE_ID
    }

def send_vote(vote, retries=3):
    """
    Sends vote to the API with retry logic to simulate
    unreliable network conditions.
    """
    global votes_sent

    if not API_URL:
        print("[ERROR] API_URL is not set in .env file!")
        return

    for attempt in range(retries):
        try:
            response = requests.post(API_URL, json=vote, timeout=5)
            if response.status_code == 200:
                votes_sent += 1  # Step 2: increment throughput counter
                print(f"[SENT] Edge: {EDGE_ID} | User: {vote['user_id']} | Choice: {vote['choice']} | Total Sent: {votes_sent}")
                return
            else:
                print(f"[RETRY {attempt+1}] Unexpected response: {response.status_code}")
        except Exception as e:
            print(f"[RETRY {attempt+1}] Failed: {e}")
            time.sleep(1)

    print(f"[FAILED] Could not send vote after {retries} attempts")

def run_edge_node():
    """
    Continuously generates and sends votes with random delays
    to simulate real-world edge behavior.
    """
    print(f"Edge node {EDGE_ID} starting...")
    while True:
        vote = generate_vote()
        send_vote(vote)
        time.sleep(random.uniform(1, 3))  # random delay between votes

if __name__ == "__main__":
    run_edge_node()