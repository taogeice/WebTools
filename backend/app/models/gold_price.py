"""
黄金价格数据模型
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, UniqueConstraint
from sqlalchemy.sql import func
from app.db.database import Base


class GoldPrice(Base):
    """黄金价格模型"""
    __tablename__ = "gold_prices"

    id = Column(Integer, primary_key=True, index=True)
    # 数据类型：国内(domestic)或国际(international)
    market_type = Column(String(20), nullable=False, index=True)
    # 日期
    date = Column(DateTime(timezone=True), nullable=False, index=True)
    # 开盘价
    open_price = Column(Float, nullable=True)
    # 最高价
    high_price = Column(Float, nullable=True)
    # 最低价
    low_price = Column(Float, nullable=True)
    # 收盘价
    close_price = Column(Float, nullable=False)
    # 最高价
    volume = Column(Float, nullable=True)
    # 创建时间
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 复合唯一索引：市场类型 + 日期
    __table_args__ = (
        UniqueConstraint('market_type', 'date', name='uix_market_date'),
    )

    def __repr__(self):
        return f"<GoldPrice(market_type={self.market_type}, date={self.date}, close_price={self.close_price})>"


class GoldPriceMetadata(Base):
    """黄金价格元数据（用于存储最后更新时间等）"""
    __tablename__ = "gold_price_metadata"

    id = Column(Integer, primary_key=True, index=True)
    market_type = Column(String(20), unique=True, nullable=False, index=True)
    last_update = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<GoldPriceMetadata(market_type={self.market_type}, last_update={self.last_update})>"
