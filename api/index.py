from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import json
import numpy as np
from statistics import mean
from pathlib import Path

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

# ✅ Correct, serverless-safe path
BASE_DIR = Path(__file__).resolve().parent
telemetry_path = BASE_DIR / "telemetry.json"

with open(telemetry_path, "r") as f:
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
