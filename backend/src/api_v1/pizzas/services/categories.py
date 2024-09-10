from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.pizzas.models import PizzaCategory


async def get_pizzas_categories(session: AsyncSession) -> list[str]:
    query = select(PizzaCategory.title).order_by(PizzaCategory.title)
    categories = await session.execute(query)
    return list(categories.scalars())
