from datetime import UTC, datetime
import uuid
from sqlmodel import Field, SQLModel, Column
import sqlalchemy.dialects.postgresql as pg
import sqlalchemy as sa


class Auth(SQLModel, table=True):
    __tablename__ = "users"
    __table_args__ = (sa.UniqueConstraint("google_id", name="uq_users_google_id"),)

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        sa_column=Column(
            pg.UUID(as_uuid=True),
            primary_key=True,
            nullable=False,
            index=True,
            server_default=sa.text("gen_random_uuid()"),
        ),
    )
    email: str = Field(
        sa_column=Column(
            pg.VARCHAR(255),
            nullable=False,
            unique=True,
            index=True,
        )
    )
    password: str | None = Field(
        default=None,
        sa_column=Column(
            pg.VARCHAR(255),
            nullable=True,
        ),
    )
    username: str = Field(
        sa_column=Column(pg.TEXT, nullable=False, unique=True, index=True)
    )
    google_id: str | None = Field(
        default=None, sa_column=Column(pg.TEXT, nullable=True, index=True)
    )
    auth_provider: str = Field(
        default="local",
        sa_column=Column(pg.TEXT, nullable=False, server_default=sa.text("'local'")),
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
            f"<Auth(id={self.id}, email={self.email}, username={self.username}, "
            f"auth_provider={self.auth_provider}, created_at={self.created_at}, "
            f"updated_at={self.updated_at})>"
        )
