from models import async_session
from models import Worker, Order
from sqlalchemy import select, update
from datetime import datetime

async def create_order(name, url, description_customer, description_ai, price_customer, price_ai, lead_time_ai):
    async with async_session() as session:
        start_data = datetime.now()
        
        session.add(Order(name=name, url=url, description_customer=description_customer, description_ai=description_ai,
                         price_customer=price_customer, price_ai=price_ai, lead_time_ai=lead_time_ai,
                        date_create = start_data))
        await session.commit()
    
async def edit_data_order(id_order, col, new_data):
    async with async_session() as session:
        await session.execute(update(Order).where(Order.id == id_order).values(**{col: new_data}))
        await session.commit()
    
async def get_data_one_order_by_url(url):
    async with async_session() as session:
        return await session.scalar(select(Order).where(Order.url == url))
    
async def get_data_one_order_by_id(id):
    async with async_session() as session:
        return await session.scalar(select(Order).where(Order.id == id))

async def get_data_all_user():
    async with async_session() as session:
        res =  await session.execute(select(Worker))
        return res.scalars().all()
    
async def get_data_one_worker_by_id(id):
    async with async_session() as session:
        return await session.scalar(select(Worker).where(Worker.id == id))