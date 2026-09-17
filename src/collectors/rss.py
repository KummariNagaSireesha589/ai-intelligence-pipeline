import aiohttp
import feedparser
from ..models import EntityRecord, Source
from ..utils.dates import parse_published, is_fresh

async def collect_feed(name: str, feed_url: str, record_type: str, hours=24):
    async with aiohttp.ClientSession(headers={"User-Agent": "ai-intelligence-pipeline/1.0"}) as session:
        async with session.get(feed_url, timeout=45) as response:
            response.raise_for_status()
            text = await response.text()
    feed = feedparser.parse(text)
    records = []
    for entry in feed.entries:
        raw_date = entry.get("published") or entry.get("updated") or entry.get("created")
        dt = parse_published(raw_date)
        if not is_fresh(dt, hours):
            continue
        records.append(EntityRecord(recordType=record_type, source=Source(name=name, url=entry.link), content={
            "title": entry.get("title", ""),
            "url": entry.link,
            "date": dt.isoformat(),
            "text": entry.get("summary", ""),
        }))
    return records
