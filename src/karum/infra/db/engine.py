from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from .uow import UoW


def create_engine(db_url: str) -> AsyncEngine:
    return create_async_engine(
        db_url,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
        echo=False,
        pool_recycle=3600
    )

def create_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine, expire_on_commit=False, autoflush=False)

def build_uow(db_url: str) -> UoW:

    # Create egnine and session factory
    engine = create_engine(db_url)
    sf = create_session_factory(engine)
    return UoW(session_factory=sf)
