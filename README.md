# Social Media Studio

Social Media Studio is a backend service that turns one stored blog post into platform-specific social media variants, sends them through a human review workflow, schedules approved variants, and publishes them safely through a shared publisher interface.

The project focuses on reliable publishing rather than only content generation.

A retry must not publish the same scheduled post twice, an unapproved variant cannot be scheduled, and scheduled work remains recoverable after an application restart.

## Features

* Blog post ingestion from Markdown or URL
* PostgreSQL persistence
* Platform-specific social variants
* Constraint validation
* Draft / approved / rejected / published workflow
* Human editing and approval
* Scheduled publishing
* Idempotency keys
* Durable schedule storage
* Publish history
* Real Discord publishing
* Mock X publisher
* Mock LinkedIn publisher
* Automated reliability tests
* Docker-based setup

## Architecture

```text
Blog post
    |
    v
Ingest + store
    |
    v
Variant generation
    |
    v
Constraint validation
    |
    v
Human review
draft -> approved / rejected
    |
    v
Schedule
    |
    v
Durable scheduler
    |
    v
SocialPublisher
    |
    +-- DiscordPublisher
    +-- MockXPublisher
    +-- MockLinkedInPublisher
    |
    v
Publish history
```

## Publisher Adapter Architecture

All platforms implement one interface:

```python
publish(
    content: str,
    idempotency_key: str,
) -> PublishResult
```

Current adapters:

```text
DiscordPublisher      real
MockXPublisher         mock
MockLinkedInPublisher  mock
```

The core publishing service does not contain Discord-, X-, or LinkedIn-specific logic.

Adding or replacing a platform happens through the adapter layer.

## Platform Constraints

### X

```text
Maximum length: 280
Maximum hashtags: 2
Tone: concise
```

### LinkedIn

```text
Maximum length: 1300
Maximum hashtags: 5
Tone: professional
```

### Discord

```text
Maximum length: 2000
Maximum hashtags: 5
Tone: conversational
```

Generated and edited variants must pass validation before continuing through the workflow.

## Review Workflow

Variants move through:

```text
draft
  |
  +--> approved --> published
  |
  +--> rejected
```

Only an approved variant can be scheduled.

Editing a variant returns it to `draft`, requiring approval again.

## Idempotency

Every schedule gets a deterministic idempotency key based on:

```text
variant ID + scheduled time
```

Before a publish operation is executed, publish history is checked for an existing successful attempt.

If the schedule has already been published successfully, the existing result is returned rather than publishing again.

This makes retries safe.

## Durable Scheduling

Schedule slots are stored in PostgreSQL.

The scheduler periodically looks for:

```text
status = pending
scheduled_for <= current time
```

If the API stops before a scheduled publish, the schedule remains in PostgreSQL.

When the application starts again, overdue pending schedules are discovered and processed.

## Tech Stack

* Python
* FastAPI
* SQLAlchemy
* PostgreSQL
* APScheduler
* HTTPX
* Discord Webhooks
* pytest
* Docker
* Docker Compose

## Project Structure

```text
app/
├── api/
├── core/
├── models/
├── publishers/
├── repositories/
├── schemas/
├── services/
└── main.py

tests/
├── conftest.py
├── test_constraints.py
├── test_publishing.py
└── test_scheduling.py

BUILDLOG.md
DESIGN.md
EVIDENCE.md
Dockerfile
docker-compose.yml
requirements.txt
```

## Setup

Clone the repository:

```bash
git clone https://github.com/Ladinski/flyrank-capstone-social-studio.git
cd flyrank-capstone-social-studio
```

Create `.env` from `.env.example`.

Example:

```env
DATABASE_URL=postgresql+psycopg://socialstudio:socialstudio@localhost:5432/socialstudio
OPENAI_API_KEY=
DISCORD_WEBHOOK_URL=your_discord_webhook_url
```

The Discord webhook must belong to a Discord server and channel you own.

Never commit the real `.env` file.

## Run with Docker

Start the full application:

```bash
docker compose up --build
```

Open Swagger:

```text
http://localhost:8000/docs
```

Stop the application:

```bash
docker compose down
```

## Basic Workflow

### 1. Create a post

```text
POST /posts
```

Example:

```json
{
  "title": "Building Reliable AI Systems",
  "markdown": "# Building Reliable AI Systems\n\nAI systems need validation, monitoring, and clear boundaries.",
  "url": null
}
```

### 2. Generate variants

```text
POST /variants/generate/{post_id}
```

The application generates variants for:

```text
x
linkedin
discord
```

### 3. Review a variant

Approve:

```text
POST /variants/{variant_id}/approve
```

Reject:

```text
POST /variants/{variant_id}/reject
```

Edit:

```text
PATCH /variants/{variant_id}/edit
```

### 4. Schedule an approved variant

```text
POST /schedules/variants/{variant_id}
```

Example:

```json
{
  "scheduled_for": "2026-08-30T18:00:00Z"
}
```

Attempting to schedule a draft or rejected variant returns HTTP 400.

### 5. Automatic Publishing

The background scheduler checks PostgreSQL for due schedules.

When a Discord schedule becomes due, the real message is sent automatically through the configured Discord webhook.

X and LinkedIn variants use mock adapters.

### 6. Publish History

View all attempts:

```text
GET /history
```

View one schedule:

```text
GET /history/schedules/{schedule_id}
```

## Testing

Run:

```bash
pytest -v
```

The tests cover important reliability behavior including:

* character constraint enforcement
* hashtag constraint enforcement
* valid variants passing validation
* refusing unapproved scheduling
* duplicate publish protection

## Reliability Guarantees

The application is designed around several important guarantees:

**Unapproved content does not publish.**

Scheduling checks the variant status before accepting work.

**Retries do not intentionally create another successful publish.**

Successful publish history is checked before calling an adapter again.

**Schedules survive application restarts.**

Schedules live in PostgreSQL rather than only in process memory.

**Platform logic stays isolated.**

The publishing service depends on the `SocialPublisher` interface rather than a specific social platform.

## Documentation

See:

```text
DESIGN.md
```

for architecture and design decisions.

See:

```text
EVIDENCE.md
```

for requirement evidence.

See:

```text
BUILDLOG.md
```

for implementation notes and AI usage.

## Known Limitations

* X and LinkedIn are mock publishers only.
* Discord is the only real publishing integration.
* Content generation currently uses deterministic templates rather than an AI model.
* URL ingestion stores the fetched response body and does not currently perform advanced article extraction.
* This project does not include engagement analytics or image generation.
