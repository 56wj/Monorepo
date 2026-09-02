import hashlib
import json
import math
import re
from collections import Counter
from pathlib import Path
from typing import Dict, Iterable, List

from .models import KnowledgeDocument, SearchHit


ASCII_TOKEN = re.compile(r"[A-Za-z][A-Za-z0-9_-]*|\d+(?:\.\d+)?")
HAN_SEQUENCE = re.compile(r"[\u4e00-\u9fff]+")


def tokenize(text: str) -> List[str]:
    normalized = text.lower()
    tokens = ASCII_TOKEN.findall(normalized)
    for sequence in HAN_SEQUENCE.findall(normalized):
        tokens.extend(sequence)
        tokens.extend(sequence[index:index + 2] for index in range(len(sequence) - 1))
    return tokens


class RuleRetriever:
    def __init__(self, documents: Iterable[KnowledgeDocument], k1: float = 1.5, b: float = 0.75):
        self.documents = list(documents)
        if not self.documents:
            raise ValueError("knowledge corpus is empty")
        self.k1 = k1
        self.b = b
        self.term_frequencies = [Counter(tokenize(self._index_text(doc))) for doc in self.documents]
        self.lengths = [sum(values.values()) for values in self.term_frequencies]
        self.average_length = sum(self.lengths) / len(self.lengths)
        self.document_frequency = Counter()
        for frequencies in self.term_frequencies:
            self.document_frequency.update(frequencies.keys())
        canonical = "\n".join(
            f"{doc.document_id}|{doc.version}|{doc.title}|{doc.text}"
            for doc in self.documents
        )
        self.corpus_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()[:16]
        self.rule_version = max(doc.version for doc in self.documents)

    @classmethod
    def from_json(cls, path: Path) -> "RuleRetriever":
        raw = json.loads(path.read_text(encoding="utf-8"))
        documents = [KnowledgeDocument(**item) for item in raw["documents"]]
        return cls(documents)

    def search(self, query: str, top_k: int = 4) -> List[SearchHit]:
        query_terms = Counter(tokenize(query))
        scored = []
        for index, document in enumerate(self.documents):
            score = self._score(index, query_terms)
            if score > 0:
                scored.append(SearchHit(
                    document_id=document.document_id,
                    title=document.title,
                    text=document.text,
                    source=document.source,
                    version=document.version,
                    score=score,
                ))
        scored.sort(key=lambda item: (-item.score, item.document_id))
        return scored[:max(1, min(top_k, 10))]

    def _score(self, index: int, query_terms: Dict[str, int]) -> float:
        frequencies = self.term_frequencies[index]
        length = self.lengths[index]
        score = 0.0
        total = len(self.documents)
        for term, query_frequency in query_terms.items():
            frequency = frequencies.get(term, 0)
            if frequency == 0:
                continue
            document_frequency = self.document_frequency[term]
            inverse_document_frequency = math.log(
                1 + (total - document_frequency + 0.5) / (document_frequency + 0.5)
            )
            denominator = frequency + self.k1 * (
                1 - self.b + self.b * length / self.average_length
            )
            score += query_frequency * inverse_document_frequency * (
                frequency * (self.k1 + 1) / denominator
            )
        return score

    @staticmethod
    def _index_text(document: KnowledgeDocument) -> str:
        return " ".join([document.title, document.text, " ".join(document.tags)])
