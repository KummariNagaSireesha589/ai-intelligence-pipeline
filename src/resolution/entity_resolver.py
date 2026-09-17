import re
from difflib import SequenceMatcher
from ..models import MappingLog

class EntityResolver:
    def __init__(self, canonical_names: list[str]):
        self.names = canonical_names
        self.aliases = {self._norm(n): n for n in canonical_names}

    @staticmethod
    def _norm(name: str) -> str:
        s = name.lower().replace("&", "and")
        s = re.sub(r"\b(incorporated|inc|llc|ltd|corp|corporation)\b", "", s)
        return re.sub(r"[^a-z0-9]", "", s)

    def resolve(self, raw: str) -> tuple[str, MappingLog]:
        key = self._norm(raw)
        if key in self.aliases:
            canonical = self.aliases[key]
            return canonical, MappingLog(raw_name=raw, canonical_name=canonical, method="exact-normalized", confidence=1.0)
        best, score = None, 0.0
        for name in self.names:
            s = SequenceMatcher(None, key, self._norm(name)).ratio()
            if s > score:
                best, score = name, s
        if best and score >= 0.90:
            return best, MappingLog(raw_name=raw, canonical_name=best, method="fuzzy", confidence=round(score, 3))
        return raw.strip(), MappingLog(raw_name=raw, canonical_name=raw.strip(), method="unresolved", confidence=0.0)
