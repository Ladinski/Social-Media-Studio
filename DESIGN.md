# Social Media Studio — Design

## Problem

Social Media Studio turns one stored blog post into platform-specific social media variants.

The system needs to handle more than text generation. A user must be able to review each generated variant, approve or reject it, schedule approved content, and safely publish it without duplicate posts.

The main reliability requirement is idempotency. Retrying a publish operation must never create a second social media post.

## Core Flow

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
SocialPublisher
    |
    +-- DiscordPublisher
    +-- MockXPublisher
    +-- MockLinkedInPublisher
    |
    v
Publish history
```

## Data Model

### Post

Stores the original content.

Fields:

* id
* title
* source_type
* source_url
* content
* created_at

The stored post is the source of truth. Variant generation reads from this stored content.

### Variant

Stores a platform-specific version of a post.

Fields:

* id
* post_id
* platform
* content
* status
* created_at
* updated_at

Valid workflow statuses:

```text
draft
approved
rejected
published
```

### ScheduleSlot

Represents one publishing slot for a variant.

Fields:

* id
* variant_id
* scheduled_for
* status
* idempotency_key
* created_at

The combination of variant and scheduled time is unique.

Each slot also receives a deterministic SHA-256 idempotency key.

### PublishAttempt

Stores publishing history.

Fields:

* id
* schedule_slot_id
* platform
* status
* external_post_id
* external_url
* error_message
* created_at

A successful attempt is checked before another publish is allowed.

## Constraint Profiles

### X

* Maximum length: 280 characters
* Maximum hashtags: 2
* Tone: concise

### LinkedIn

* Maximum length: 1300 characters
* Maximum hashtags: 5
* Tone: professional

### Discord

* Maximum length: 2000 characters
* Maximum hashtags: 5
* Tone: conversational

Constraints are enforced by application code before a generated or edited variant can continue through the workflow.

## Publisher Interface

All publishing implementations use the same interface:

```python
publish(
    content: str,
    idempotency_key: str,
) -> PublishResult
```

Implementations:

* `DiscordPublisher` — real Discord webhook publishing
* `MockXPublisher` — simulated X publishing
* `MockLinkedInPublisher` — simulated LinkedIn publishing

Business logic interacts with the publisher interface rather than platform-specific APIs.

## Idempotency

Every scheduled variant has an idempotency key derived from:

```text
variant ID + scheduled time
```

Before publishing, the service checks whether the schedule already has a successful publish attempt.

If one exists, that existing result is returned instead of publishing again.

This protects against API retries and scheduler retries.

## Durable Scheduling

Schedule slots are stored in PostgreSQL.

The scheduler periodically searches PostgreSQL for:

```text
status = pending
scheduled_for <= current time
```

If the application stops, the scheduled work remains in PostgreSQL.

After restart, overdue pending schedules are discovered and processed.

The publishing idempotency check prevents completed schedules from being published twice.

## API Surface

### Posts

```text
POST /posts
GET  /posts/{post_id}
```

### Variants

```text
POST /variants/generate/{post_id}
GET  /variants/post/{post_id}
GET  /variants/{variant_id}

PATCH /variants/{variant_id}/edit
POST  /variants/{variant_id}/approve
POST  /variants/{variant_id}/reject
```

### Scheduling

```text
POST /schedules/variants/{variant_id}
GET  /schedules/{schedule_id}
```

### Publishing

```text
POST /publish/schedules/{schedule_id}
```

### Publish History

```text
GET /history
GET /history/schedules/{schedule_id}
```

## Explicit Non-Goal

The project does not attempt to publish to real X, LinkedIn, or Instagram accounts.

X and LinkedIn are deliberately implemented as mock adapters. Discord is used as the real publishing target.

Analytics, engagement tracking, and image generation are also outside the scope of this project.
