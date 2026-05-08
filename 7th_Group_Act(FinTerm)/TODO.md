# Distributed Voting System — Group TODO

> **Stack:** Python + FastAPI + Supabase (PostgreSQL)  
> **Replace GCP with:** Supabase (Pub/Sub → vote_queue table, Firestore → votes table)

---

## PHASE 1 — Supabase Setup

- [ ] Go to [supabase.com](https://supabase.com) and create an account
- [ ] Create a new project named `cs323-voting-system-groupX`
  - Region: Southeast Asia (Singapore)
  - Save your database password
- [ ] Go to **Settings → API** and copy:
  - [ ] Project URL → paste into `.env` as `SUPABASE_URL`
  - [ ] Service Role Key → paste into `.env` as `SUPABASE_KEY`
- [ ] Go to **SQL Editor → New Query** and run the table creation SQL:
  - [ ] `vote_queue` table created
  - [ ] `votes` table created
- [ ] Go to **Table Editor** and confirm both tables appear

---

## PHASE 2 — Project Files Setup

- [ ] Create project folder on your computer
- [ ] Create these 4 files inside the folder:
  - [ ] `.env` — fill in SUPABASE_URL, SUPABASE_KEY, API_URL
  - [ ] `api.py` — FastAPI ingestion layer
  - [ ] `worker.py` — processing/worker service
  - [ ] `edge_node.py` — edge node simulation
- [ ] Open terminal and install dependencies:
  ```
  pip install fastapi uvicorn supabase requests python-dotenv
  ```
- [ ] Each group member sets their own `edge_id` in `edge_node.py`:
  - Member 1 → `"edge_id": "node_1"`
  - Member 2 → `"edge_id": "node_2"`
  - Member 3 → `"edge_id": "node_3"`
  - Member 4 → `"edge_id": "node_4"`
  - Member 5 → `"edge_id": "node_5"`

---

## PHASE 3 — Run the System (Normal Operation)

- [ ] Open **Terminal 1** — run the API:
  ```
  python -m uvicorn api:app --reload --port 8000
  ```
- [ ] Open **Terminal 2** — run the worker:
  ```
  python worker.py
  ```
- [ ] Open **Terminal 3** — run the edge node:
  ```
  python edge_node.py
  ```
- [ ] Confirm Terminal 1 shows: `POST /vote HTTP/1.1 200 OK`
- [ ] Confirm Terminal 2 shows: `[PROCESSED] uuid | Poll: poll_1`
- [ ] Confirm Terminal 3 shows: `[SENT] uuid | Choice: A/B/C`
- [ ] Go to Supabase **Table Editor** and confirm:
  - [ ] `vote_queue` table has rows coming in
  - [ ] `votes` table has processed votes

---

## PHASE 4 — Fault Injection Testing

### Test 1: Message Duplication
- [ ] In `edge_node.py`, modify send to send same vote twice:
  ```python
  vote = generate_vote()
  send_vote(vote)
  send_vote(vote)  # intentional duplicate
  ```
- [ ] Run the edge node and observe:
  - [ ] `vote_queue` receives duplicate rows
  - [ ] `votes` table still has NO duplicates (idempotency works)
- [ ] Revert the change after testing

### Test 2: Worker Failure
- [ ] Stop `worker.py` (press `Ctrl+C` in Terminal 2)
- [ ] Keep `edge_node.py` running
- [ ] Observe in Supabase:
  - [ ] `vote_queue` keeps accumulating unprocessed rows
  - [ ] `votes` table stops updating
  - [ ] API keeps accepting votes normally
- [ ] Run this SQL to count the backlog:
  ```sql
  SELECT COUNT(*) FROM vote_queue WHERE processed = FALSE;
  ```

### Test 3: Worker Recovery
- [ ] Restart `worker.py` in Terminal 2
- [ ] Observe:
  - [ ] Worker automatically processes all queued votes
  - [ ] `votes` table resumes updating
  - [ ] No manual intervention needed

---

## PHASE 5 — Performance Analysis

- [ ] Measure latency — check worker terminal for latency logs
- [ ] Run this SQL to compare vote counts across layers:
  ```sql
  SELECT
    (SELECT COUNT(*) FROM vote_queue) AS total_received,
    (SELECT COUNT(*) FROM vote_queue WHERE processed = TRUE) AS total_processed,
    (SELECT COUNT(*) FROM votes) AS total_stored;
  ```
- [ ] Take note of:
  - [ ] Average latency (edge → Supabase)
  - [ ] Throughput during normal operation
  - [ ] Queue buildup during worker downtime
  - [ ] Recovery speed after worker restarts

---

## PHASE 6 — Submission Preparation

- [ ] Write `README.md` containing:
  - [ ] System overview and architecture explanation
  - [ ] Step-by-step setup and execution instructions
  - [ ] Individual reflection from each member (paragraph form)
- [ ] Include architecture diagram (use the one generated in chat)
- [ ] Record a demo GIF or short video showing:
  - [ ] Edge node generating votes
  - [ ] API receiving votes
  - [ ] Worker processing votes
  - [ ] Supabase tables updating in real time
- [ ] Organize GitHub repository:
  ```
  repo/
  ├── .env.example       (do NOT upload real .env)
  ├── api.py
  ├── worker.py
  ├── edge_node.py
  ├── README.md
  ├── TODO.md
  └── architecture.png
  ```
- [ ] Push all files to GitHub
- [ ] Submit GitHub repository link to teacher

---

## Individual Reflections Checklist (each member)

Each member writes a paragraph covering:
- [ ] Difference between sequential vs distributed execution
- [ ] How the system behaved under normal, failure, and recovery conditions
- [ ] Challenges faced during implementation
- [ ] Insights on message buffering, idempotency, and eventual consistency
- [ ] When distributed execution helped vs when it added complexity

---

> **Tip:** Keep all 3 terminals running at the same time during testing.  
> **Tip:** Never upload your real `.env` file to GitHub — add it to `.gitignore`.