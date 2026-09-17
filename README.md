# AI Intelligence Pipeline

Production-oriented demo implementation for the AI Engineer assessment.

The pipeline is designed around the assessment requirements: asynchronous ingestion, source traceability, 24-hour freshness checks, multi-tier LLM extraction with 413/429 handling, deterministic entity resolution, GitHub enrichment, and scale-out architecture for 500k+ records.

> **Data integrity:** the repository never invents source records. Every emitted entity is required to retain a source URL. Demo fixtures are explicitly marked as fixtures; production runs consume configured public sources/APIs.

## Structure

```text
src/
  config.py
  models.py
  pipeline.py
  collectors/
    arxiv.py
    rss.py
  llm/
    orchestrator.py
  resolution/
    entity_resolver.py
  storage/
    jsonl.py
  utils/
    dates.py
    retry.py
architecture.pdf
config.example.yaml
requirements.txt
```

## Quick start

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
python -m src.pipeline --config config.example.yaml --out data
```

Set provider keys only when enabling the LLM extraction tier. The deterministic pipeline can run without an LLM key.

## Assessment mapping

- Phase I: concurrent source collectors and paginated acquisition; adapters are stateless so workers can be horizontally scaled.
- Phase II: RSS/HTML date normalization and strict 24-hour filtering.
- Phase III: Gemini Flash -> Groq Llama -> DeepSeek fallback, bounded chunking, exponential backoff + jitter for 429/5xx responses.
- Phase IV: normalized exact/alias matching with a canonical seed map and auditable mapping logs.
- Phase V: Playwright-ready browser adapter is intentionally isolated; robots/terms-aware crawling is preferred over CAPTCHA bypassing.
- Phase VI: PostgreSQL for canonical entities/events, object storage for raw payloads, and Neo4j/pgvector as optional relationship layers.

## Important limitation of this demo

The assessment asks for 1,000 startups, 1,000 products, and 1,000 papers plus a public Google Sheet. This repository contains the reusable acquisition pipeline rather than fabricated rows. Run it against the configured legitimate sources to produce the submission dataset. The Google Form is intentionally not populated with invented links or metrics.
