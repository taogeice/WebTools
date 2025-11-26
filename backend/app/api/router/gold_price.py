"""
黄金价格路由
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime, timedelta

from app.api.dependencies.deps import get_db
from app.services.gold_price_service import GoldPriceService
from app.schemas.gold_price import GoldPrice, GoldPriceResponse, DateRangeQuery, MarketSummary
from app.models.gold_price import GoldPrice as GoldPriceModel

router = APIRouter()


@router.post("/sync", response_model=Dict[str, str])
async def sync_gold_price_data(
    query: DateRangeQuery,
    db: Session = Depends(get_db)
):
    """
    同步黄金价格数据（从 API 获取并保存到数据库）
    """
    service = GoldPriceService(db)

    # 同步国内数据
    domestic_result = service.sync_gold_price_data(
        market_type='domestic',
        start_date=query.start_date,
        end_date=query.end_date
    )

    # 同步国际数据
    international_result = service.sync_gold_price_data(
        market_type='international',
        start_date=query.start_date,
        end_date=query.end_date
    )

    return {
        "status": "success",
        "message": "数据同步完成",
        "domestic": domestic_result,
        "international": international_result
    }


@router.get("/data/{market_type}", response_model=GoldPriceResponse)
async def get_gold_price_data(
    market_type: str,
    start_date: Optional[str] = Query(None, description="开始日期 (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="结束日期 (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """
    获取黄金价格数据
    :param market_type: 市场类型 (domestic/international)
    """
    # 验证市场类型
    if market_type not in ['domestic', 'international']:
        raise HTTPException(status_code=400, detail="市场类型必须是 'domestic' 或 'international'")

    # 如果没有提供日期，默认获取最近30天
    if not start_date:
        start_date = datetime.now() - timedelta(days=30)
    else:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')

    if not end_date:
        end_date = datetime.now()
    else:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

    # 从数据库获取数据
    service = GoldPriceService(db)
    data = service.get_data_from_db(market_type, start_date, end_date)

    if not data:
        # 如果数据库中没有数据，尝试同步
        sync_result = service.sync_gold_price_data(market_type, start_date, end_date)
        data = service.get_data_from_db(market_type, start_date, end_date)

        if not data:
            raise HTTPException(
                status_code=404,
                detail="未找到数据，请先同步数据"
            )

    return GoldPriceResponse(
        market_type=market_type,
        data=data,
        start_date=start_date,
        end_date=end_date,
        total_count=len(data)
    )


@router.get("/summary/{market_type}", response_model=MarketSummary)
async def get_market_summary(
    market_type: str,
    db: Session = Depends(get_db)
):
    """
    获取市场汇总信息（最新价格和变化）
    """
    if market_type not in ['domestic', 'international']:
        raise HTTPException(status_code=400, detail="市场类型必须是 'domestic' 或 'international'")

    # 获取最近两天的数据
    service = GoldPriceService(db)
    today = datetime.now()
    yesterday = today - timedelta(days=3)  # 往前多取一点以确保有数据

    data = service.get_data_from_db(market_type, yesterday, today)

    if len(data) < 1:
        raise HTTPException(status_code=404, detail="未找到足够的数据")

    latest = data[-1]
    previous = data[-2] if len(data) > 1 else None

    change = None
    change_percent = None
    if previous:
        change = latest.close_price - previous.close_price
        change_percent = (change / previous.close_price) * 100

    return MarketSummary(
        market_type=market_type,
        latest_price=latest.close_price,
        previous_price=previous.close_price if previous else None,
        change=change,
        change_percent=change_percent,
        volume=latest.volume
    )


@router.get("/comparison")
async def compare_markets(
    start_date: Optional[str] = Query(None, description="开始日期 (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="结束日期 (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """
    比较国内和国际市场数据
    """
    # 如果没有提供日期，默认获取最近7天
    if not start_date:
        start_date = datetime.now() - timedelta(days=7)
    else:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')

    if not end_date:
        end_date = datetime.now()
    else:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

    service = GoldPriceService(db)

    domestic_data = service.get_data_from_db('domestic', start_date, end_date)
    international_data = service.get_data_from_db('international', start_date, end_date)

    return {
        "status": "success",
        "start_date": start_date,
        "end_date": end_date,
        "domestic": {
            "market_type": "domestic",
            "data_count": len(domestic_data),
            "data": domestic_data
        },
        "international": {
            "market_type": "international",
            "data_count": len(international_data),
            "data": international_data
        }
    }


@router.get("/latest")
async def get_latest_prices(db: Session = Depends(get_db)):
    """
    获取最新的国内外黄金价格
    """
    service = GoldPriceService(db)
    today = datetime.now()
    week_ago = today - timedelta(days=10)

    domestic_data = service.get_data_from_db('domestic', week_ago, today)
    international_data = service.get_data_from_db('international', week_ago, today)

    result = {}

    if domestic_data:
        latest = domestic_data[-1]
        result['domestic'] = {
            'market_type': 'domestic',
            'price': latest.close_price,
            'date': latest.date
        }

    if international_data:
        latest = international_data[-1]
        result['international'] = {
            'market_type': 'international',
            'price': latest.close_price,
            'date': latest.date
        }

    return {
        "status": "success",
        "data": result,
        "timestamp": datetime.now()
    }


@router.get("/metadata")
async def get_metadata(db: Session = Depends(get_db)):
    """
    获取数据库元数据
    """
    from app.models.gold_price import GoldPriceMetadata

    metadata = db.query(GoldPriceMetadata).all()

    result = []
    for meta in metadata:
        result.append({
            "market_type": meta.market_type,
            "last_update": meta.last_update
        })

    return {
        "status": "success",
        "metadata": result
    }
