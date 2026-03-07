# Solutions

## Task 1: Health Check

**What I found:**
The API was missing a health check endpoint, and Docker did not have a way to know if the FastAPI app and its Redis dependency were fully functional. The Python slim image also lacked `curl` for the Docker `healthcheck` command to use.

**What I did:**
1. Added a `GET /health` endpoint to `app/main.py`. This endpoint pings Redis and returns the application uptime. It purposely raises a `HTTP 503` if Redis is unreachable.
2. Updated `app/Dockerfile` to install `curl` via `apt-get`.
3. Updated `docker-compose.yml` by adding a Docker `healthcheck` property to the `api` service. The check runs `curl -f http://localhost:8000/health` so that an HTTP `503` results in an exit code `1`, accurately reflecting an unhealthy state if Redis is down.

**Why:**
We need health checks so that orchestrators like Docker/Kubernetes can safely restart sick containers or hold off routing traffic to them until they are fully booted and fully connected to crucial dependencies (like Redis).

---

## Task 2: Fix Staging Environment

**What I found:**

**What I did:**

**Why:**

---

## Task 3: Incident Investigation

See `INCIDENT.md`

---

## Production Readiness

> If this project had to run in production serving real users, what are 3 things you'd change or add?

1.
2.
3.
