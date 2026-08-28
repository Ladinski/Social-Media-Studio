# Social Media Studio — Build Log

## Project Setup

I started the project with Python and FastAPI and created a separate structure for API routes, services, repositories, database models, schemas, and publisher adapters.

PostgreSQL runs through Docker and stores the application state.

I used AI assistance to help plan the initial project structure and generate parts of the implementation. I reviewed and tested the code while building each phase.

## Post Ingestion

I added support for storing a blog post from Markdown or a URL.

The stored post became the source used by variant generation instead of passing the original request directly through the system.

## Variant Generation

I first implemented deterministic templates for X and LinkedIn.

I chose templates instead of immediately using an AI API because generation itself is not the reliability problem this project is testing. Templates also made constraint behavior predictable while building the rest of the system.

Discord generation was added when the real Discord publisher was implemented.

## Constraint Validation

I created platform profiles for maximum length, tone, and hashtag limits.

One issue appeared during testing because a Markdown heading such as:

```text
# Building Reliable AI Systems
```

was incorrectly counted as a social media hashtag.

I changed the variant generator to clean Markdown headings before validation.

After the change, the generated X variant correctly passed its two-hashtag limit.

## Human Review

I added draft, approved, rejected, and published statuses.

The user can approve, reject, or edit a variant.

An edited variant returns to draft so the changed content must be approved again.

The scheduling service refuses any variant that is not approved.

## Publisher Architecture

I added a common `SocialPublisher` interface and a publisher factory.

The first two implementations were mock X and mock LinkedIn publishers.

They allowed the publishing workflow to be developed without using real restricted social media APIs.

## Discord Integration

I chose Discord as the real free publishing target.

The Discord adapter uses a webhook URL stored in `.env`.

During the first real test, publishing returned:

```text
Discord webhook URL is not configured.
```

The webhook had been added after the FastAPI process started. Restarting the application caused the settings to reload correctly.

After restarting, a real message was successfully published to Discord.

## Idempotency

Each schedule receives an idempotency key generated from the variant ID and scheduled time.

Before publishing, the service checks publish history for an existing successful attempt.

If one exists, the existing attempt is returned.

This prevents repeated API calls from creating duplicate posts.

## Scheduling

I added a scheduler that searches PostgreSQL for pending schedules whose publishing time has passed.

PostgreSQL is used as the durable source of truth rather than keeping scheduled work only in process memory.

This means schedules remain available after an application restart.

The existing idempotent publishing layer protects against duplicate publishes during retries.

## Publish History

Every publishing attempt is stored with its result.

The history records success or failure, platform, external ID, external URL, errors, and timestamp.

API endpoints expose the complete history and history for an individual schedule.

## Testing

I added tests for the highest-risk behavior:

* X character limits
* X hashtag limits
* valid constraints
* refusing to schedule draft variants
* repeated publishing producing one successful result

These tests focus on the reliability rules that would be most damaging if they failed.

## AI Usage

AI assistance helped with:

* project structure
* FastAPI implementation
* SQLAlchemy models
* adapter architecture
* validation logic
* test design
* documentation

I did not treat generated code as automatically correct.

One concrete example was the original hashtag validation interaction with Markdown headings. Testing exposed the problem and the generation logic was changed before continuing.

I also manually tested the real Discord integration and the project workflow through FastAPI's Swagger interface.
