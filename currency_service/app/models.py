import asyncpg
import logging
from datetime import datetime, timedelta

from sqlalchemy import and_
from sqlalchemy.sql.expression import func

from db import db

logger = logging.getLogger(__name__)


class Currency(db.Model):
    __tablename__ = 'currency'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Unicode(length=50), unique=True, nullable=False)

    @classmethod
    async def get_or_create(cls, name: str) -> 'Currency':
        get_query = cls.query.where(cls.name == name)
        result = await get_query.gino.first()
        if not result:
            try:
                result = await cls.create(name=name)
            except asyncpg.UniqueViolationError:
                result = await get_query.gino.first()
        return result


class Rate(db.Model):
    __tablename__ = 'rate'
    __table_args__ = (
        db.UniqueConstraint('currency_id', 'date'),
    )

    id = db.Column(db.Integer(), primary_key=True)
    currency_id = db.Column(db.Integer(), db.ForeignKey('currency.id'), nullable=False)
    date = db.Column(db.DateTime(timezone=True), nullable=False)
    rate = db.Column(db.Numeric(), nullable=False)
    volume = db.Column(db.Numeric(), nullable=False)

    @classmethod
    async def update_or_create(cls, currency_id, date, rate, volume) -> None:
        update_query = cls.update.values(
            rate=rate, volume=volume,
        ).where(
            and_(cls.currency_id == currency_id, cls.date == date),
        )
        update, _ = await update_query.gino.status()
        if update == 'UPDATE 0':  # TODO find a better way to check if nothing was found
            try:
                await cls.create(currency_id=currency_id, date=date, rate=rate, volume=volume)
            except asyncpg.UniqueViolationError:
                await update_query.gino.status()

    @classmethod
    async def get_last_rate(cls, currency_id):
        return await cls.query.where(
            and_(cls.currency_id == currency_id),
        ).order_by(cls.date.desc()).gino.first()

    @classmethod
    async def get_avg_volume(cls, currency_id: int, last_days=None):
        query = func.avg(cls.volume).select().where(cls.currency_id == currency_id)
        if last_days:
            last_days_dt = datetime.utcnow().replace(
                hour=0, minute=0, second=0, microsecond=0,
            ) - timedelta(days=last_days - 1)
            query = query.where(Rate.date >= last_days_dt)
        return await query.gino.scalar()
