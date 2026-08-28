# Social Media Studio — Evidence

This document records evidence for the main Social Media Studio requirements.

## 1. Post Ingestion

Endpoint:

```text
POST /posts
```

Example input:

```json
{
  "title": "Building Reliable AI Systems",
  "markdown": "# Building Reliable AI Systems\n\nAI systems need validation, monitoring, and clear boundaries.",
  "url": null
}
```

Result:

The post is stored in PostgreSQL and receives an ID. All later variant generation uses the stored post.

---

## 2. Platform Constraint Enforcement

Automated tests:

```text
tests/test_constraints.py::test_x_variant_over_character_limit_is_blocked
tests/test_constraints.py::test_x_variant_over_hashtag_limit_is_blocked
tests/test_constraints.py::test_valid_x_variant_passes
```

Expected test result:

```text
PASSED
PASSED
PASSED
```

Example rejected variant:

```text
x hashtag limit exceeded: 3/2.
```

This proves platform constraints are enforced in code before review.

---

## 3. Review Workflow

Supported statuses:

```text
draft
approved
rejected
published
```

Endpoints:

```text
PATCH /variants/{variant_id}/edit
POST  /variants/{variant_id}/approve
POST  /variants/{variant_id}/reject
```

Editing a variant returns it to `draft`, requiring another approval.

Published variants cannot be edited, rejected, or re-approved.

---

## 4. Unapproved Variants Cannot Be Scheduled

Automated test:

```text
tests/test_scheduling.py::test_unapproved_variant_cannot_be_scheduled
```

Expected result:

```text
PASSED
```

Example API error:

```json
{
  "detail": "Only approved variants can be scheduled. Current status: draft."
}
```

The endpoint returns HTTP 400.

---

## 5. Publisher Adapter Layer

The application uses one `SocialPublisher` interface.

Implementations:

```text
DiscordPublisher
MockXPublisher
MockLinkedInPublisher
```

The publishing service selects an adapter through `PublisherFactory`.

Platform-specific API logic does not exist in the core publishing workflow.

---

## 6. Real Platform Publishing

Real target:

```text
Discord webhook
```

A Discord variant was approved, scheduled, and successfully sent to a Discord server owned by the developer.

Successful publish records include:

```text
platform = discord
status = success
external_post_id = Discord message ID
external_url = Discord message URL
```

The live Discord message confirms that the real adapter works.

---

## 7. Idempotent Publishing

Automated test:

```text
tests/test_publishing.py::test_repeated_publish_returns_one_success
```

The test calls the same schedule publishing operation twice.

Expected result:

```text
PASSED
```

Both calls resolve to the same successful publish attempt.

The publish history contains exactly:

```text
1 successful attempt
```

This proves that retrying a successful schedule does not create another post.

---

## 8. Durable Scheduling

Schedule slots are stored in PostgreSQL.

The background scheduler checks for:

```text
pending schedules
scheduled_for <= current time
```

Restart test:

1. Create and approve a Discord variant.
2. Schedule it for a future time.
3. Stop the application before the scheduled time.
4. Allow the scheduled time to pass.
5. Restart the application.
6. The overdue schedule is discovered.
7. One Discord message is published.
8. No duplicate message is created.

This demonstrates that scheduled work survives an application restart.

---

## 9. Publish History

Endpoints:

```text
GET /history
GET /history/schedules/{schedule_id}
```

Each publish attempt records:

```text
schedule
platform
status
external post ID
external URL
error message
timestamp
```

Both successes and failures are visible.

---

## 10. Secrets

Real secrets are stored only in:

```text
.env
```

The repository ignores `.env`.

Safe placeholders are provided in:

```text
.env.example
```

Values include:

```text
DATABASE_URL
OPENAI_API_KEY
DISCORD_WEBHOOK_URL
```
