import asyncio
import aiohttp
import feedparser
from ..models import EntityRecord, Source

ARXIV_API = "https://export.arxiv.org/api/query"

async def fetch_papers(query="cat:cs.AI", start=0, max_results=100):
    params = {"search_query": query, "start": start, "max_results": max_results, "sortBy": "submittedDate", "sortOrder": "descending"}
    async with aiohttp.ClientSession(headers={"User-Agent": "ai-intelligence-pipeline/1.0"}) as session:
        async with session.get(ARXIV_API, params=params, timeout=60) as response:
            response.raise_for_status()
            text = await response.text()
    feed = feedparser.parse(text)
    out = []
    for e in feed.entries:
        out.append(EntityRecord(recordType="RESEARCH_PAPER", source=Source(name="arXiv", url=e.link), content={
            "title": e.title.strip(),
            "authors": [a.name for a in e.authors],
            "paper_url": e.link,
            "github_url": None,
            "github_stars": None,
            "published_date": e.published,
        }))
    return out

async def collect_concurrently(queries, page_size=100):
    return [r for batch in await asyncio.gather(*(fetch_papers(q, 0, page_size) for q in queries)) for r in batch]
