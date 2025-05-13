"""
Created_by: Rakesh
Created date: 12/05/2025
Modified date:
"""
import json
from datetime import datetime

from cachetools import TTLCache
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
import logging

from app.db.session import get_db
from app.schemas.jobs import JobsListResponse
from app.services.user_service import get_filtered_and_paginated_jobs

cache = TTLCache(maxsize=100, ttl=600)  # can store 100 items and last for 10 minutes
logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/jobs", response_model=JobsListResponse)
async def fetch_all_users(
    name: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    try:
        start_time = datetime.now().strftime('%H:%M:%S')
        logger.info(f"__Jobs Data fetch started at {start_time}")
        response = get_filtered_and_paginated_jobs(db, name, page, page_size)
        end_time = datetime.now().strftime('%H:%M:%S')
        logger.info(f"__ Jobs Data fetch ended at {end_time}")
        return response

    except Exception as e:
        print(f"Error in fetch_all_jobs: {e}")
        raise HTTPException(status_code=500, detail="Could not fetch jobs")
