import asyncio

class LLMOrchestrator:
    """Provider-neutral fallback chain. Wire provider SDKs through the small _call_* methods."""
    def __init__(self, providers=None, max_chars=24000):
        self.providers = providers or ["gemini", "groq", "deepseek"]
        self.max_chars = max_chars

    def chunk(self, text: str, overlap=500):
        text = text or ""
        if len(text) <= self.max_chars:
            return [text]
        chunks, step = [], max(1, self.max_chars - overlap)
        for i in range(0, len(text), step):
            chunks.append(text[i:i+self.max_chars])
        return chunks

    async def extract(self, text: str, schema: dict):
        errors = []
        for provider in self.providers:
            for chunk in self.chunk(text):
                try:
                    return await self._call(provider, chunk, schema)
                except Exception as exc:
                    errors.append(f"{provider}: {exc}")
                    continue
        raise RuntimeError("All LLM providers failed: " + "; ".join(errors))

    async def _call(self, provider, chunk, schema):
        # Provider SDK integration belongs here. A production adapter should retry 429/5xx
        # with exponential backoff and treat 413 as a signal to reduce chunk size.
        raise NotImplementedError(f"Configure provider adapter: {provider}")
