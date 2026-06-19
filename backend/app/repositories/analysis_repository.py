from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.analysis import Analysis, AnalysisStatus


class AnalysisRepository:

    async def get_by_id(self, db: AsyncSession, analysis_id: UUID) -> Analysis | None:
        result = await db.execute(
            select(Analysis).where(Analysis.id == analysis_id)
        )
        return result.scalar_one_or_none()

    async def get_all_for_user(
        self, db: AsyncSession, user_id: UUID
    ) -> list[Analysis]:
        result = await db.execute(
            select(Analysis)
            .where(Analysis.user_id == user_id)
            .order_by(Analysis.created_at.desc())
        )
        return list(result.scalars().all())

    async def create(
        self, db: AsyncSession, repo_id: UUID, user_id: UUID
    ) -> Analysis:
        analysis = Analysis(
            repo_id=repo_id,
            user_id=user_id,
            status=AnalysisStatus.PENDING,
            progress=0,
        )
        db.add(analysis)
        await db.commit()
        await db.refresh(analysis)
        return analysis

    async def update_progress(
        self,
        db: AsyncSession,
        analysis_id: UUID,
        progress: int,
        current_step: str,
        status: str | None = None,
    ) -> None:
        analysis = await self.get_by_id(db, analysis_id)
        if not analysis:
            return
        analysis.progress = progress
        analysis.current_step = current_step
        if status:
            analysis.status = status
        await db.commit()

    async def mark_completed(
        self, db: AsyncSession, analysis_id: UUID, **result_fields
    ) -> Analysis:
        analysis = await self.get_by_id(db, analysis_id)
        analysis.status = AnalysisStatus.COMPLETED
        analysis.progress = 100
        analysis.current_step = "Done"
        analysis.completed_at = datetime.now(timezone.utc)
        for key, value in result_fields.items():
            setattr(analysis, key, value)
        await db.commit()
        await db.refresh(analysis)
        return analysis

    async def mark_failed(
        self, db: AsyncSession, analysis_id: UUID, error_message: str
    ) -> None:
        analysis = await self.get_by_id(db, analysis_id)
        if analysis:
            analysis.status = AnalysisStatus.FAILED
            analysis.error_message = error_message
            await db.commit()


analysis_repository = AnalysisRepository()
