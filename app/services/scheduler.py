import logging
from datetime import datetime, timezone

from apscheduler.schedulers.background import BackgroundScheduler

from app.core.database import SessionLocal
from app.repositories.schedule_repository import ScheduleRepository
from app.services.publishing import PublishingService


logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler(
    timezone="UTC",
)


def process_due_schedules():
    db = SessionLocal()

    try:
        now = datetime.now(timezone.utc).replace(tzinfo=None)

        schedules = ScheduleRepository.get_due(
            db,
            now,
        )

        for schedule in schedules:
            try:
                logger.info(
                    "Publishing schedule %s",
                    schedule.id,
                )

                PublishingService.publish_schedule(
                    db,
                    schedule.id,
                )

            except Exception:
                logger.exception(
                    "Failed to publish schedule %s",
                    schedule.id,
                )

    finally:
        db.close()


def start_scheduler():
    if scheduler.running:
        return

    scheduler.add_job(
        process_due_schedules,
        trigger="interval",
        seconds=10,
        id="process_due_schedules",
        replace_existing=True,
        max_instances=1,
    )

    scheduler.start()


def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown()