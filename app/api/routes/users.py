"""
Created_by: Rakesh
Created date: 05/05/2025
Modified date: 07/05/2025
"""
import json
from datetime import datetime, time
from cachetools import TTLCache
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
import logging

from app.db.session import get_db
from app.schemas.user import UsersListResponse
from app.services.user_service import get_filtered_and_paginated_users

cache = TTLCache(maxsize=100, ttl=600)  # can store 100 items and last for 10 minutes
logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/", response_model=UsersListResponse)
async def fetch_all_users(
    name: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    try:
        start_time = datetime.now().strftime('%H:%M:%S')
        logger.info(f"__ User Data fetch started at {start_time}")
        # print(f"user fetch started at {start_time}__")
        response = get_filtered_and_paginated_users(db, name, page, page_size)
        end_time = datetime.now().strftime('%H:%M:%S')
        logger.info(f"__ User Data fetch ended at {end_time}")
        return response

    except Exception as e:
        print(f"Error in fetch_all_users: {e}")
        raise HTTPException(status_code=500, detail="Could not fetch users")

#
# @router.get("/user/{user_id}", response_model=UserData)
# async def get_user(user_id: int, db: Session = Depends(get_db)):
#     logger.info(f"Fetching user by ID: {user_id}")
#
#     try:
#         start_time = datetime.now().strftime('%H:%M:%S')
#         logger.info(f"__ User Details fetch started at {start_time}")
#         user = get_user_by_id(db, user_id)
#         if not user:
#             raise HTTPException(status_code=404, detail="User not found")
#         response = UserData(id=user.id, name=user.name, email=user.email, role=user.role)
#         end_time = datetime.now().strftime('%H:%M:%S')
#         logger.info(f"__ User Data fetch ended at {end_time}")
#         return response
#
#     except HTTPException as he:
#         raise he
#     except Exception as e:
#         logger.error(f"Error in get_user: {e}")
#         raise HTTPException(status_code=500, detail="Could not fetch user")