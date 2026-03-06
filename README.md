# DevOps Trainee — Take-Home Assignment

## Scenario

You just joined as a DevOps trainee. Your senior engineer is on leave for 2 days. He left you a small project the team maintains, and **3 tickets** to finish before he's back.

The project is a simple **URL shortener API** built with FastAPI, running behind NGINX, and using Redis for storage. Everything runs in Docker.

---

## Getting Started

```bash
# Clone your repo (created from this template)
git clone <your-repo-url>
cd devops-trainee-assignment

# Start the project
docker compose up --build
```

The app should be accessible at `http://localhost:8080`

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/shorten` | Shorten a URL. Body: `{"url": "https://example.com"}` |
| GET | `/{short_code}` | Redirect to original URL |
| GET | `/stats/{short_code}` | Get click stats for a short URL |

---

## Your Tickets

### Ticket 1: Add a Health Check

The team needs a proper health check endpoint for monitoring.

**Requirements:**
- Add a `GET /health` endpoint to the API
- It should return: service status, uptime (how long the app has been running), and whether Redis is reachable or not
- Configure Docker to use this endpoint to determine if the container is healthy
- The health check should fail if Redis is not reachable

**Deliverable:** Working endpoint + Docker healthcheck configured

---

### Ticket 2: Fix the Staging Environment

The team runs this app in two environments: `dev` and `staging`. The dev environment works fine (you just tested it). Now the team needs to test in staging mode.

To switch to staging:
```bash
docker compose --env-file .env.staging up --build
```

**It breaks.** Your job is to figure out why and fix it.

There may be more than one issue. Make sure the app works correctly in staging mode.

**Deliverable:** Working staging environment + document what was wrong in `SOLUTIONS.md`

---

### Ticket 3: Investigate Last Night's Incident

Users reported the API was slow last night between 2:00 AM and 2:45 AM. The app recovered on its own after that.

A log file from that period is available at `logs/incident.log`.

Investigate the logs and write an incident report.

**Deliverable:** `INCIDENT.md` with your analysis (template provided below)

---

## Submission Requirements

### 1. Git Commits
- Work in git. **Commit as you go.** Don't squash.
- Write meaningful commit messages.
- We will review your git history.

### 2. `SOLUTIONS.md`
For each ticket, write:
- **What you found** — what was the issue?
- **What you did** — how did you fix it?
- **Why** — why was it broken in the first place?

### 3. `INCIDENT.md`
Use this template:
```markdown
## What happened
(Brief summary)

## Timeline
(What you observed in the logs, with timestamps)

## Root cause
(Why did this happen?)

## Impact
(What was the effect on users?)

## How to prevent this in the future
(What monitoring, alerts, or changes would catch this early?)
```

### 4. Production Readiness (Open-ended)
At the bottom of your `SOLUTIONS.md`, answer this:

> "If this project had to run in production serving real users, what are 3 things you'd change or add? Just list them with one line each."

---

## Rules

- **Google is your teammate.** Use it freely.
- **Don't change things that already work.** If dev mode works, it should still work after your changes.
- **Time limit:** 48 hours from when you receive this.
- **Everything you need is in this repo.** There are no hidden tricks.

---

Good luck.
