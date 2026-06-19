from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.repository import Repository


class RepoRepository:

    async def get_by_id(self, db: AsyncSession, repo_id: UUID) -> Repository | None:
        result = await db.execute(select(Repository).where(Repository.id == repo_id))
        return result.scalar_one_or_none()

    async def get_by_user_and_url(
        self, db: AsyncSession, user_id: UUID, github_url: str
    ) -> Repository | None:
        result = await db.execute(
            select(Repository).where(
                Repository.user_id == user_id,
                Repository.github_url == github_url,
            )
        )
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, *, obj_in: dict, user_id: UUID) -> Repository:
        db_obj = Repository(**obj_in, user_id=user_id)
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj

    async def get_multi_by_user(
        self, db: AsyncSession, user_id: UUID, skip: int = 0, limit: int = 100
    ) -> list[Repository]:
        result = await db.execute(
            select(Repository)
            .where(Repository.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())


repo_repository = RepoRepository()
