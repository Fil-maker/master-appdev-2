from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.orm_db import Order, Report


class ReportRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, report_id: int) -> Report | None:
        result = await self.session.execute(
            select(Report).where(Report.id == report_id)
        )
        return result.scalar_one_or_none()

    async def get_by_filter(self, count: int, page: int, **kwargs) -> list[Report]:
        """page: в человеческом формате начиная с 1"""
        offset_val = (page - 1) * count

        # Build query with optional filters
        query = select(Report)

        # Apply filters from kwargs if provided
        for key, value in kwargs.items():
            if hasattr(Report, key) and value is not None:
                if key == "report_at":
                    # value_example = '2023-10-30'
                    format_string = '%Y-%m-%d'
                    value = datetime.strptime(value, format_string)
                query = query.where(getattr(Report, key) == value)

        query = query.limit(count).offset(offset_val)
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def create(self, order_id: int) -> Report:
        result = await self.session.execute(select(Order).where(Order.id == order_id))
        order = result.scalar_one_or_none()
        # print(order.products)
        report = Report(order_id=order_id, stock_quantity=len(order.products))
        self.session.add(report)
        await self.session.commit()
        await self.session.refresh(report)
        return report
