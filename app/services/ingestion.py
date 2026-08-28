import httpx
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.post_repository import PostRepository
from app.schemas.post import PostCreate


class IngestionService:
    @staticmethod
    def ingest(db: Session, payload: PostCreate):
        if payload.markdown and payload.url:
            raise HTTPException(
                status_code=400,
                detail="Provide either markdown or url, not both.",
            )

        if not payload.markdown and not payload.url:
            raise HTTPException(
                status_code=400,
                detail="Either markdown or url is required.",
            )

        if payload.markdown:
            content = payload.markdown.strip()

            if not content:
                raise HTTPException(
                    status_code=400,
                    detail="Markdown content cannot be empty.",
                )

            return PostRepository.create(
                db,
                title=payload.title,
                source_type="markdown",
                content=content,
            )

        try:
            response = httpx.get(
                str(payload.url),
                timeout=10.0,
                follow_redirects=True,
            )
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise HTTPException(
                status_code=400,
                detail=f"Could not fetch URL: {exc}",
            )

        content = response.text.strip()

        if not content:
            raise HTTPException(
                status_code=400,
                detail="Fetched URL returned empty content.",
            )

        return PostRepository.create(
            db,
            title=payload.title,
            source_type="url",
            source_url=str(payload.url),
            content=content,
        )