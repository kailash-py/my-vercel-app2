from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json
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
with open("telemetry.json", "r") as f:
    telemetry = json.load(f)

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
