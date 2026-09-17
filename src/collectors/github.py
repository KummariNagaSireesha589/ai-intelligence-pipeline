import aiohttp
from ..utils.retry import retry_async

async def github_stars(repo_url: str) -> int | None:
    """Read current public GitHub star count without inventing a value."""
    parts = repo_url.rstrip('/').split('/')
    if len(parts) < 2:
        return None
    owner, repo = parts[-2], parts[-1]
    api = f"https://api.github.com/repos/{owner}/{repo}"
    async def call():
        async with aiohttp.ClientSession(headers={"Accept": "application/vnd.github+json", "User-Agent": "ai-intelligence-pipeline/1.0"}) as s:
            async with s.get(api, timeout=30) as r:
                if r.status in (429, 500, 502, 503, 504):
                    raise RuntimeError(f"retryable HTTP {r.status}")
                if r.status == 404:
                    return None
                r.raise_for_status()
                data = await r.json()
                return data.get("stargazers_count")
    return await retry_async(call)
