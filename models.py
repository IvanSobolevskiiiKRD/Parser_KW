from sqlalchemy import DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url="sqlite+aiosqlite:///db.sqlite3")

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class Worker(Base):
    __tablename__ = "Workers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    otklikow: Mapped[int] = mapped_column()

class Order(Base):
    __tablename__ = "Orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    url: Mapped[str] = mapped_column()
    description_customer: Mapped[str] = mapped_column()
    description_ai: Mapped[str] = mapped_column()
    price_customer: Mapped[int] = mapped_column()
    price_ai: Mapped[int] = mapped_column()
    lead_time_ai: Mapped[int] = mapped_column()
    date_create: Mapped[DateTime] = mapped_column(DateTime)
    id_worker_respons: Mapped[int] = mapped_column(nullable=True)
    answer_worker: Mapped[str] = mapped_column(nullable=True)
    price_worker: Mapped[int] = mapped_column(nullable=True)
    lead_time: Mapped[int] = mapped_column(nullable=True)



async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)