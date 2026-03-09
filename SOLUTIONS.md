# Solutions

## Task 1: Health Check

**What I found:**

API was missing a healthcheck endpoint and docker did not knew if redis and fastapi are running or not.  the python docker image also lacked curl command to check the health of the application.

**What I did:**
1. Added a `GET /health` endpoint to `app/main.py`. This endpoint pings Redis and returns the application uptime. It raises a `HTTP 503` if Redis is unreachable.
2. Updated `app/Dockerfile` to install `curl` via `apt-get`.
3. Updated `docker-compose.yml` by adding a Docker `healthcheck` property to the `api` service. The check runs `curl -f http://localhost:8000/health` so that an HTTP `503` results in an exit code `1`, so we can know if Redis is down.

**Why:**
We need health checks so that orchestrators like Docker/Kubernetes can safely restart the containers if they are not running properly.
---

## Task 2: Fix Staging Environment

**What I found:**
When we ran docker compose --env-file .env.staging up, Docker injected REDIS_HOST=redis-staging into the API container. We had defined the service name as redis in docker-compose.yml. The FastAPI application throws the redis: unreachable flag because it is trying to connect to a host hostname named redis-staging, but it literally does not exist on the internal Docker DNS.

**What I did:**
I updated `.env.staging` to use `REDIS_HOST=redis` so it accurately targets the Redis container within the Docker network.

**Why:**
When Docker creates the network, it automatically assigns a DNS hostname to every container, and that hostname is exactly the service name defined in docker-compose.yml.

---

## Task 3: Incident Investigation

See `INCIDENT.md`

---

## Production Readiness

> If this project had to run in production serving real users, what are 3 things you'd change or add?

1. **Adding a Database**: HAving Redis As a peimary Database is not good because we have seen in our application that it stores everything in memory and when it need to save to disk it performs BGSAVE and then the app degrades. SO we can use Mysql/ Postgress as our Databse to store all the data so the data writing operation is separated and also redis does not perform this. We can use Redis For caching so that if there is cache hit  it redirects instantly and if there is cache miss Redis Checks the Db and then perform the operation 

2. **Rate Limiting** : We can also use Rate limiting as there might be vulnerable endpoints from which there may be many requests coming resulting in DDOs attaks which will degrade app performance. So we can impose Rate limits on the The IP's so they can only perform X requests in Y minutes.

3. **Exposing Metrics ENdpoints** : We can also expose a metrics endpoint /metrics for our Fast api app  so we can set up monitoring using PRometheus and Grafana. We can also set up alerts on bais of metrics Like Error spikes, Request LAtency. ALso for Nginx we can use the stub_status Modules so we can monitor the Nginx performance too. This will help us to know Active connections, Reading/Writing/Waiting request states, and Total Handled Requests.
