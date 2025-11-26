"""
黄金价格 Pydantic 模型
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class GoldPriceBase(BaseModel):
    """黄金价格基础模型"""
    market_type: str = Field(..., description="市场类型：domestic(国内)或international(国际)")
    open_price: Optional[float] = Field(None, description="开盘价")
    high_price: Optional[float] = Field(None, description="最高价")
    low_price: Optional[float] = Field(None, description="最低价")
    close_price: Optional[float] = Field(..., description="收盘价")
    volume: Optional[float] = Field(None, description="成交量")


class GoldPriceCreate(GoldPriceBase):
    """创建黄金价格模型"""
    date: datetime = Field(..., description="日期")


class GoldPriceUpdate(BaseModel):
    """更新黄金价格模型"""
    open_price: Optional[float] = None
    high_price: Optional[float] = None
    low_price: Optional[float] = None
    close_price: Optional[float] = None
    volume: Optional[float] = None


class GoldPrice(GoldPriceBase):
    """黄金价格响应模型"""
    id: int
    date: datetime
    created_at: datetime

    class Config:
        orm_mode = True


class GoldPriceResponse(BaseModel):
    """黄金价格列表响应"""
    market_type: str
    data: List[GoldPrice]
    start_date: datetime
    end_date: datetime
    total_count: int


class DateRangeQuery(BaseModel):
    """日期范围查询模型"""
    start_date: datetime = Field(..., description="开始日期")
    end_date: datetime = Field(..., description="结束日期")
    market_type: Optional[str] = Field(None, description="市场类型：domestic或international")


class PriceTrend(BaseModel):
    """价格趋势"""
    date: datetime
    price: float
    change: Optional[float] = None
    change_percent: Optional[float] = None


class MarketSummary(BaseModel):
    """市场汇总"""
    market_type: str
    latest_price: float
    previous_price: Optional[float] = None
    change: Optional[float] = None
    change_percent: Optional[float] = None
    volume: Optional[float] = None
