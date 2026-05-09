-- Run this in Supabase SQL Editor before starting the system

-- vote_queue table: acts as the Pub/Sub message queue
-- Votes are inserted here by the API and polled by the worker
CREATE TABLE vote_queue (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id TEXT NOT NULL,
  poll_id TEXT NOT NULL,
  choice TEXT NOT NULL,
  timestamp FLOAT NOT NULL,
  edge_id TEXT,
  processed BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- votes table: final storage for processed votes
-- doc_id = user_id + "_" + poll_id (idempotency key)
-- processed_at is nullable — set by the worker on upsert
CREATE TABLE votes (
  doc_id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  poll_id TEXT NOT NULL,
  choice TEXT NOT NULL,
  timestamp FLOAT NOT NULL,
  edge_id TEXT,
  processed_at TIMESTAMPTZ
);

-- Optional: index for faster worker polling on unprocessed votes
CREATE INDEX IF NOT EXISTS idx_vote_queue_processed ON vote_queue (processed);