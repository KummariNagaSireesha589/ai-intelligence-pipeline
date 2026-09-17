# Technical Architecture

## 1. Scale strategy
Stateless async crawler workers consume partitioned source/cursor ranges from a queue. Source adapters are independent, so scaling from thousands to 500k+ records is an infrastructure change: add workers and queue throughput. Raw responses are stored in object storage; canonical records live in PostgreSQL.

## 2. 413 / 429 handling
The LLM orchestrator uses Gemini Flash -> Groq Llama -> DeepSeek. Requests are bounded by a configurable character/token budget. A 413 causes smaller chunks; 429/5xx errors use exponential backoff with jitter, per-provider concurrency limits, and circuit breakers.

## 3. Freshness and deduplication
Publication dates are normalized to UTC. News and jobs are accepted only when their publication timestamp is within 24 hours. A deterministic fingerprint from source URL + normalized content/date is stored under a unique constraint so distributed workers can retry safely without duplicates.

## 4. Storage
PostgreSQL is the canonical system of record. Object storage retains raw HTML/API responses for auditability. Neo4j can represent startup/founder/product/paper relationships; pgvector can provide semantic retrieval when keeping the vector layer inside PostgreSQL is preferable.

## 5. Anti-bot and scale thinking
Prefer official APIs, RSS, sitemaps and permitted public pages. Respect robots.txt, terms and rate limits. For JavaScript-rendered pages, use an asynchronous Playwright adapter where permitted. Do not defeat CAPTCHAs or access controls; use an authorized source/API instead.

## 6. Observability and data quality
Log source, URL, latency, retry count, HTTP status, parser version and record fingerprint. Track freshness rejection, duplicates, extraction success, LLM fallback rate and GitHub enrichment coverage. Every emitted record retains a legitimate source URL; fabricated records are not used.
