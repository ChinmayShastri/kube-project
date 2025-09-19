from fastapi import FastAPI, Request
import time
import random
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

app = FastAPI()

REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method','endpoint','http_status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'Request latency seconds', ['endpoint'])

# simple queue gauge simulated
from prometheus_client import Gauge
QUEUE_SIZE = Gauge('app_queue_size', 'Simulated background queue size')

@app.get("/health")
async def health():
    return {"status":"ok"}

@app.get("/api/message")
async def message():
    endpoint = "/api/message"
    start = time.time()
    # simulate variable processing and optional queue push/pop
    # simulate queue size
    q = random.randint(0, 30)
    QUEUE_SIZE.set(q)

    # simulate processing latency
    processing = random.uniform(0.05, 0.7)  # seconds
    time.sleep(processing)

    latency = time.time() - start
    REQUEST_LATENCY.labels(endpoint=endpoint).observe(latency)
    REQUEST_COUNT.labels(method="GET", endpoint=endpoint, http_status="200").inc()

    return {"message": "Hello from backend", "processing_time": processing, "queue": q}

@app.get("/metrics")
async def metrics():
    resp = generate_latest()
    return Response(content=resp, media_type=CONTENT_TYPE_LATEST)
