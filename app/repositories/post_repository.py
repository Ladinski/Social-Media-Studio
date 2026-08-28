from sqlalchemy.orm import Session

from app.models.post import Post


class PostRepository:
    @staticmethod
    def create(
        db: Session,
        *,
        title: str,
        source_type: str,
        content: str,
        source_url: str | None = None,
    ) -> Post:
        post = Post(
            title=title,
            source_type=source_type,
            source_url=source_url,
            content=content,
        )

        db.add(post)
        db.commit()
        db.refresh(post)

        return post

    @staticmethod
    def get_by_id(db: Session, post_id: int) -> Post | None:
        return db.get(Post, post_id)