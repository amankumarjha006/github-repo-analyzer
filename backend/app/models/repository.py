import uuid
from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlalchemy import BigInteger, ForeignKey, String, func, Boolean, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.analysis import Analysis


class Repository(Base):
    """Repository ORM model."""

    __tablename__ = "repositories"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    github_id: Mapped[int] = mapped_column(
        BigInteger,
        index=True,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    owner: Mapped[str] = mapped_column(String(255), nullable=False)
    github_url: Mapped[str] = mapped_column(String(512), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    stars_count: Mapped[int] = mapped_column(default=0, nullable=False)
    forks_count: Mapped[int] = mapped_column(default=0, nullable=False)
    open_issues_count: Mapped[int] = mapped_column(default=0, nullable=False)

    # Added columns
    full_name: Mapped[str] = mapped_column(String(300), nullable=False, index=True)
    primary_language: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    watchers_count: Mapped[int] = mapped_column(default=0, nullable=False)
    size_kb: Mapped[Optional[int]] = mapped_column(nullable=True)
    is_private: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    is_fork: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    default_branch: Mapped[str] = mapped_column(String(100), default="main", server_default="main")
    license_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    homepage_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    last_pushed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    created_on_github: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    last_fetched_at: Mapped[datetime] = mapped_column(server_default=func.now())

    # Topics and metadata
    topics: Mapped[Optional[list[str]]] = mapped_column(
        ARRAY(String),
        nullable=True,
    )
    github_metadata: Mapped[Optional[dict]] = mapped_column(
        JSONB,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="repositories")
    analyses: Mapped[list["Analysis"]] = relationship(
        "Analysis",
        back_populates="repository",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Repository {self.owner}/{self.name}>"
