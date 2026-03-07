import os
import string
import random
import time
from datetime import datetime

import redis
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

app = FastAPI(title="URL Shortener")

START_TIME = time.time()

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


class URLRequest(BaseModel):
    url: str


def generate_code(length=6):
    chars = string.ascii_letters + string.digits
    return "".join(random.choices(chars, k=length))


@app.post("/shorten")
def shorten_url(request: URLRequest):
    code = generate_code()
    r.set(f"url:{code}", request.url)
    r.set(f"clicks:{code}", 0)
    r.set(f"created:{code}", datetime.now().isoformat())
    return {"short_code": code, "short_url": f"/{code}"}


@app.get("/stats/{short_code}")
def get_stats(short_code: str):
    url = r.get(f"url:{short_code}")
    if not url:
        raise HTTPException(status_code=404, detail="Short URL not found")
    clicks = r.get(f"clicks:{short_code}")
    created = r.get(f"created:{short_code}")
    return {
        "short_code": short_code,
        "original_url": url,
        "clicks": int(clicks) if clicks else 0,
        "created_at": created,
    }


@app.get("/health")
def health_check():
    uptime = time.time() - START_TIME
    try:
        # Check if Redis is reachable
        r.ping()
        redis_status = "reachable"
    except redis.ConnectionError:
        redis_status = "unreachable"

    response = {
        "status": "healthy" if redis_status == "reachable" else "unhealthy",
        "uptime_seconds": round(uptime, 2),
        "redis": redis_status
    }

    # Fail the health check with a 503 if Redis is unreachable
    if redis_status == "unreachable":
        raise HTTPException(status_code=503, detail=response)

    return response


@app.get("/{short_code}")
def redirect_to_url(short_code: str):
    url = r.get(f"url:{short_code}")
    if not url:
        raise HTTPException(status_code=404, detail="Short URL not found")
    r.incr(f"clicks:{short_code}")
    return RedirectResponse(url=url)
