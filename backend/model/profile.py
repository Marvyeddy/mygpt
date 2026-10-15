from datetime import UTC, datetime
from typing import Optional
import uuid
import sqlalchemy as sa
from sqlmodel import Column, Field, SQLModel
import sqlalchemy.dialects.postgresql as pg


class Profile(SQLModel, table=True):
    __tablename__ = "profiles"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(
            pg.UUID(as_uuid=True),
            nullable=False,
            primary_key=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
    )

    user_id: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
            index=True,
        )
    )
    avatar_url: Optional[str] = Field(
        default=None, sa_column=Column(pg.TEXT, nullable=True)
    )
    display_name: Optional[str] = Field(
        sa_column=Column(pg.VARCHAR(100), nullable=True)
    )
    tier: str = Field(
        default="free",
        sa_column=Column(
            pg.VARCHAR(50), nullable=False, server_default=sa.text("'free'")
        ),
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column=Column(
            pg.TIMESTAMP(timezone=True), nullable=False, server_default=sa.func.now()
        ),
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column=Column(
            pg.TIMESTAMP(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
        ),
    )

    def __repr__(self):
        return (
            f"<Profile(id={self.id}, user_id={self.user_id}, display_name={self.display_name}, "
            f"avatar_url={self.avatar_url}, tier={self.tier}, "
            f"created_at={self.created_at}, updated_at={self.updated_at})>"
        )
