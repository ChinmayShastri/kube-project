from fastapi import FastAPI
from fastapi.responses import Response
import random
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST

app = FastAPI()

# Define custom metrics
processing_time_gauge = Gauge(
    "backend_processing_time_seconds",
    "Time spent processing requests"
)
queue_gauge = Gauge(
    "backend_queue_size",
    "Current queue size"
)

@app.get("/api/message")
def get_message():
    processing_time = random.random()
    queue = random.randint(1, 20)

    # Update Prometheus gauges
    processing_time_gauge.set(processing_time)
    queue_gauge.set(queue)

    return {
        "message": "Hello from backend",
        "processing_time": processing_time,
        "queue": queue
    }

@app.get("/metrics")
def metrics():
    # Proper Response with correct Content-Type for Prometheus
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.get("/health")
def health():
    # Optional health endpoint for K8s probes
    return {"status": "ok"}