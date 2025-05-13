"""
Created_by: Rakesh
Created date: 05/05/2025
Modified date: 07/05/2025
"""

import json
import logging
import time
from typing import Optional
from cachetools import TTLCache
from sqlalchemy.orm import Session

from app.crud.jobs import get_jobs
from app.crud.user import get_users
from app.schemas.jobs import JobsData
from app.schemas.user import UserData

logger = logging.getLogger(__name__)
cache = TTLCache(maxsize=100, ttl=600)  # can store 100 items and last for 10 minutes

# fetch data and store in cache
def set_cache_data(db: Session, cache_id):
    start_time = time.time()
    logger.info("Data fetch started from Database")

    try:
        if cache_id == 'user_json_test':
            users = get_users(db, skip=0)
            user_dicts = [{"id": u.id, "name": u.name, "email": u.email, "role": u.role} for u in users]
            cache[cache_id] = json.dumps(user_dicts)
            duration = time.time() - start_time
            logger.info(f"Data fetch and saved to cache completed in {duration:.3f} seconds")
            return user_dicts
        else:
            jobs = get_jobs(db, skip=0)
            logger.info(f"Data fetch completed")
            jobs_dicts = [{"id": u.id, "title": u.title, "company": u.company, "location": u.location} for u in jobs]
            cache[cache_id] = json.dumps(jobs_dicts)
            duration = time.time() - start_time
            logger.info(f"Data fetch and saved to cache completed in {duration:.3f} seconds")
            return jobs_dicts

    except Exception as e:
        logger.error(f"Failed to fetch user data: {e}")
        raise

def apply_filters(data, name: Optional[str]):
    return [
        user for user in data
        if not name or name.lower() in user["name"].lower()
        # if not id or id in user["id"]
    ]

def paginate(data, page: int, page_size: int):
    start = (page - 1) * page_size
    end = start + page_size
    return data[start:end]

def get_filtered_and_paginated_users(db: Session, name: Optional[str], page: int, page_size: int):
    start = time.time()
    if "user_json_test" in cache:
        logger.info("Returning users from cache")
        users = json.loads(cache["user_json_test"])
    else:
        logger.info("No cache found. Fetching from DB")
        users = set_cache_data(db,'user_json_test')

    filtered_users = apply_filters(users, name)
    paginated_users = paginate(filtered_users, page, page_size)
    end = time.time() - start
    logger.info(f"data fetched in {end:.4f}")


    return {
        "total": len(filtered_users),
        "page": page,
        "page_size": page_size,
        "users": [UserData(**user) for user in paginated_users]
    }

def get_filtered_and_paginated_jobs(db: Session, name: Optional[str], page: int, page_size: int):
    start = time.time()
    if "job_json_test" in cache:
        logger.info("Returning jobs from cache")
        jobs = json.loads(cache["job_json_test"])
    else:
        logger.info("No cache found. Fetching from DB")
        jobs = set_cache_data(db,'job_json_test')
        logger.info("Fetching jobs from DB completed")

    # filtered_jobs = apply_filters(jobs, name)
    paginated_jobs = paginate(jobs, page, page_size)
    end = time.time() - start
    logger.info(f"data fetched in {end:.4f}")

    return {
        "total": len(jobs),
        "page": page,
        "page_size": page_size,
        "jobs": [JobsData(**job) for job in paginated_jobs]
    }


# fetch data and store in cache
# def set_jobs_cache(db: Session):
#     start_time = time.time()
#     logger.info("Data fetch started from Database")
#
#     try:
#         jobs = get_jobs(db, skip=0)
#         logger.info(f"Data fetch completed")
#         jobs_dicts = [{"id": u.id, "title": u.title, "company": u.company, "location": u.location} for u in jobs]
#         cache["job_json_test1"] = json.dumps(jobs_dicts)
#         duration = time.time() - start_time
#         logger.info(f"Data fetch and saved to cache completed in {duration:.3f} seconds")
#         return jobs_dicts
#     except Exception as e:
#         logger.error(f"Failed to fetch Jobs data: {e}")
#         raise

# def get_users_data_by_id(db: Session,user_id: int):
#         start = time.time()
#         logger.info(f"Fetching userdata started at {start:.4f}")
#         if "user_json_test" in cache:
#             logger.info("Returning users from cache")
#             users = json.loads(cache["user_json_test"])
#         else:
#             logger.info("No cache found. Fetching from DB")
#             users = set_cache_data(db)
#
#         filtered_users = apply_filters(users, id)
#         end = time.time() - start
#         logger.info(f"data fetched in {end:.4f}")
#         return {
#             "users": [UserData(**user) for user in users]
#         }