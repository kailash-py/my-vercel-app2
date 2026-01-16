from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from statistics import mean

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Load telemetry data
telemetry = [
    {"region": "amer", "latency_ms": 120, "uptime": 0.99},
    {"region": "amer", "latency_ms": 150, "uptime": 0.98},
    {"region": "amer", "latency_ms": 200, "uptime": 1.0},
    {"region": "apac", "latency_ms": 100, "uptime": 0.97},
    {"region": "apac", "latency_ms": 160, "uptime": 0.95},
    {"region": "apac", "latency_ms": 180, "uptime": 0.96},
    {"region": "emea", "latency_ms": 140, "uptime": 0.98},
    {"region": "emea", "latency_ms": 170, "uptime": 0.99},
    {"region": "emea", "latency_ms": 190, "uptime": 0.97}
]

@app.post("/analytics")
async def analytics(request: Request):
    body = await request.json()
    regions = body["regions"]
    threshold = body["threshold_ms"]

    response = {}

    for region in regions:
        records = [r for r in telemetry if r["region"] == region]

        latencies = [r["latency_ms"] for r in records]
        uptimes = [r["uptime"] for r in records]

        response[region] = {
            "avg_latency": round(mean(latencies), 2),
            "p95_latency": round(np.percentile(latencies, 95), 2),
            "avg_uptime": round(mean(uptimes), 4),
            "breaches": len([l for l in latencies if l > threshold])
        }

    return response

@app.get("/analytics")
def analytics_get(regions: str = "amer,apac", threshold_ms: int = 156):
    region_list = regions.split(",")
    threshold = threshold_ms

    response = {}

    for region in region_list:
        records = [r for r in telemetry if r["region"] == region]

        latencies = [r["latency_ms"] for r in records]
        uptimes = [r["uptime"] for r in records]

        response[region] = {
            "avg_latency": round(mean(latencies), 2),
            "p95_latency": round(np.percentile(latencies, 95), 2),
            "avg_uptime": round(mean(uptimes), 4),
            "breaches": len([l for l in latencies if l > threshold])
        }

    return response
