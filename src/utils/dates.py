from datetime import datetime, timezone, timedelta
import re
from dateutil import parser

RELATIVE = re.compile(r"^(\d+)\s+(minute|minutes|hour|hours|day|days)\s+ago$", re.I)

def parse_published(value: str | None, now: datetime | None = None) -> datetime | None:
    if not value:
        return None
    now = now or datetime.now(timezone.utc)
    m = RELATIVE.match(value.strip())
    if m:
        n, unit = int(m.group(1)), m.group(2).lower()
        seconds = n * (60 if "minute" in unit else 3600 if "hour" in unit else 86400)
        return now - timedelta(seconds=seconds)
    try:
        dt = parser.parse(value)
        return dt.replace(tzinfo=dt.tzinfo or timezone.utc)
    except (ValueError, OverflowError):
        return None

def is_fresh(dt: datetime | None, hours: int = 24, now: datetime | None = None) -> bool:
    if not dt:
        return False
    now = now or datetime.now(timezone.utc)
    dt = dt.astimezone(timezone.utc)
    return timedelta(0) <= now - dt <= timedelta(hours=hours)
