### Distributed Voting System - Supabase Architecture:
```mermaid

graph TD
    N1[Node 1\nedge_node.py] -->|HTTP POST /vote| API
    N2[Node 2\nedge_node.py] -->|HTTP POST /vote| API
    N3[Node 3\nedge_node.py] -->|HTTP POST /vote| API
    N4[Node 4\nedge_node.py] -->|HTTP POST /vote| API
    N5[Node N\nedge_node.py] -->|HTTP POST /vote| API

    API[FastAPI — Ingestion API\napi.py · port 8000\nValidates vote]

    API -->|INSERT row| Q[(vote_queue table\nprocessed = false)]

    Q -->|Poll every 2s| W[Worker service\nworker.py\nDeduplicates]

    W -->|UPSERT doc_id| V[(votes table\ndoc_id = user_id + poll_id)]
    W -->|processed = true| Q

    subgraph Supabase [Supabase replaces GCP]
        Q
        V
    end

```

---

### Antonio's Reflection:
Implementing the distributed voting system using Supabase gave me a hands-on understanding of how distributed systems handle data across multiple independent components. I observed that unlike sequential execution, distributed execution allowed multiple edge nodes to generate and send votes simultaneously, which made the system faster but also introduced challenges in managing duplicate messages and ensuring data consistency. During the fault injection testing, I noticed that stopping the worker service caused votes to accumulate in the vote_queue table, but once the worker was restored, it automatically processed all queued votes without any manual intervention, which demonstrated the concept of eventual consistency. One of the biggest challenges I encountered was configuring the Supabase connection and ensuring that the API, worker, and edge nodes communicated correctly, especially when debugging asynchronous behavior across three separate terminals. Overall, this activity deepened my understanding of how real-world distributed systems use message queuing, idempotency, and fault tolerance to remain reliable even when individual components fail.

---

### Casia's Reflection:
Working on this distributed voting system helped me better understand how distributed systems work in real-world environments. Our group used Supabase, I learned how cloud databases and asynchronous processing can still achieve reliable communication between edge nodes, APIs, and worker services. One thing I noticed was that distributed execution is more complex than normal sequential programs because multiple components run independently and failures can happen at different parts of the system. During testing, I observed that even when the worker service stopped, votes were still queued and processed once the service recovered, which showed the importance of fault tolerance and message buffering. Overall, this activity helped me understand the trade-offs between scalability, reliability, and system complexity in distributed computing.