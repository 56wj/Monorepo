from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class PlanningRequest:
    query: str
    order_context: Dict[str, Any] = field(default_factory=dict)
    top_k: int = 4
    trace_id: Optional[str] = None


@dataclass(frozen=True)
class KnowledgeDocument:
    document_id: str
    title: str
    text: str
    tags: List[str]
    source: str
    version: str


@dataclass(frozen=True)
class SearchHit:
    document_id: str
    title: str
    text: str
    source: str
    version: str
    score: float

    def to_dict(self) -> Dict[str, Any]:
        value = asdict(self)
        value["score"] = round(self.score, 6)
        return value
