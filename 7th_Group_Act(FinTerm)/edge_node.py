import uuid, random, time, requests, os
from dotenv import load_dotenv

load_dotenv()
API_URL = os.getenv("API_URL")

def generate_vote():
    return {
        "user_id": str(uuid.uuid4()),
        "poll_id": "poll_1",
        "choice": random.choice(["A", "B", "C"]),
        "timestamp": time.time(),
        "edge_id": "node_den_jester_antonio"
    }

def send_vote(vote, retries=3):
    for attempt in range(retries):
        try:
            response = requests.post(API_URL, json=vote, timeout=5)
            if response.status_code == 200:
                print(f"[SENT] {vote['user_id']} | Choice: {vote['choice']}")
                return
        except Exception as e:
            print(f"[RETRY {attempt+1}] Failed: {e}")
            time.sleep(1)
    print(f"[FAILED] Could not send vote after {retries} attempts")

def run_edge_node():
    while True:
        vote = generate_vote()
        send_vote(vote)
        time.sleep(random.uniform(1, 3))

if __name__ == "__main__":
    run_edge_node()