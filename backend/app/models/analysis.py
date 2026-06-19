import uuid
from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlalchemy import ForeignKey, String, func, Integer, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.repository import Repository


class AnalysisStatus:
    PENDING    = "pending"
    PROCESSING = "processing"
    COMPLETED  = "completed"
    FAILED     = "failed"


class EmbeddingStatus:
    PENDING    = "pending"
    PROCESSING = "processing"
    READY      = "ready"
    FAILED     = "failed"


class Analysis(Base):
    """Analysis ORM model."""

    __tablename__ = "analyses"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    repo_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("repositories.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    status: Mapped[str] = mapped_column(
        String(50),
        default="pending",
        nullable=False,
        index=True,
    )
    error_message: Mapped[Optional[str]] = mapped_column(
        String(1024),
        nullable=True,
    )

    # Status tracking section
    progress: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    current_step: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # AI results (written by the background task)
    tech_stack: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    folder_structure: Mapped[Optional[dict]] = mapped_column(JSONB, nullable=True)
    architecture_summary: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    project_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # Scores 0-100
    quality_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    security_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    documentation_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    complexity_score: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Metrics
    files_analyzed: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    total_files: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    lines_of_code: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Embedding pipeline (needed for RAG chat in Phase 2)
    embedding_status: Mapped[str] = mapped_column(
        String(20), default="pending", server_default="pending"
    )
    embedding_chunks: Mapped[int] = mapped_column(Integer, default=0, server_default="0")

    # Timestamps
    started_at: Mapped[datetime] = mapped_column(server_default=func.now())
    completed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="analyses")
    repository: Mapped["Repository"] = relationship("Repository", back_populates="analyses")

    def __repr__(self) -> str:
        return f"<Analysis {self.id} (status={self.status})>"
