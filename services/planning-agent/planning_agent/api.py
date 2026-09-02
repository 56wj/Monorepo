import logging
import re
import time
import uuid
from typing import Any, Dict

from fastapi import FastAPI, Request
from pydantic import BaseModel, ConfigDict, Field
from prometheus_client import Counter, Histogram, make_asgi_app

from .engine import PlanningAgent
from .models import PlanningRequest


LOG = logging.getLogger("planning-agent")
TRACE_ID = re.compile(r"[A-Za-z0-9._-]{8,64}")
PLAN_REQUESTS = Counter(
    "packing_agent_plan_requests_total",
    "Planning agent requests",
    ["outcome", "job_type"],
)
PLAN_LATENCY = Histogram(
    "packing_agent_plan_duration_seconds",
    "Planning agent end-to-end latency",
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2),
)
RETRIEVAL_HITS = Histogram(
    "packing_agent_retrieval_hits",
    "Grounded rule hits returned per plan",
    buckets=(0, 1, 2, 3, 4, 6, 8, 10),
)


class PlanInput(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    query: str = Field(min_length=1, max_length=4000)
    order_context: Dict[str, Any] = Field(default_factory=dict, alias="orderContext")
    top_k: int = Field(default=4, ge=1, le=10, alias="topK")

class SearchInput(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    query: str = Field(min_length=1, max_length=1000)
    top_k: int = Field(default=4, ge=1, le=10, alias="topK")

app = FastAPI(title="Packing Planning Agent", version="2.0.0")
app.mount("/metrics", make_asgi_app())
agent = PlanningAgent.from_corpus()


@app.middleware("http")
async def trace_requests(request: Request, call_next):
    supplied = request.headers.get("X-Trace-Id", "")
    trace_id = supplied if TRACE_ID.fullmatch(supplied) else uuid.uuid4().hex
    request.state.trace_id = trace_id
    response = await call_next(request)
    response.headers["X-Trace-Id"] = trace_id
    return response


@app.get("/healthz")
def health() -> Dict[str, Any]:
    return {
        "status": "UP",
        "ruleVersion": agent.retriever.rule_version,
        "corpusHash": agent.retriever.corpus_hash,
        "documentCount": len(agent.retriever.documents),
    }


@app.post("/v1/knowledge/search")
def search(payload: SearchInput) -> Dict[str, Any]:
    hits = agent.retriever.search(payload.query, payload.top_k)
    return {
        "ruleVersion": agent.retriever.rule_version,
        "corpusHash": agent.retriever.corpus_hash,
        "hits": [hit.to_dict() for hit in hits],
    }


@app.post("/v1/plans")
def plan(payload: PlanInput, request: Request) -> Dict[str, Any]:
    started = time.perf_counter()
    result = agent.plan(PlanningRequest(
        query=payload.query,
        order_context=payload.order_context,
        top_k=payload.top_k,
        trace_id=request.state.trace_id,
    ))
    outcome = "executable" if result["decision"]["executable"] else "draft"
    job_type = result["decision"]["jobType"]
    PLAN_REQUESTS.labels(outcome=outcome, job_type=job_type).inc()
    RETRIEVAL_HITS.observe(len(result["citations"]))
    PLAN_LATENCY.observe(time.perf_counter() - started)
    LOG.info(
        "plan_completed trace_id=%s request_hash=%s outcome=%s job_type=%s",
        request.state.trace_id,
        result["requestHash"],
        outcome,
        job_type,
    )
    return result
