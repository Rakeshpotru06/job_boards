"""
    Created_by: Rakesh
    created date: 05/05/2025
    Modified date: 06/05/2025
"""
import hashlib
import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import logging
from app.crud.user import get_users
from app.db.session import get_db
from app.schemas.user import Usersdata
import time
import orjson
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel

router = APIRouter()
logger = logging.getLogger(__name__)
cache = {}
CACHE_TTL = 600 #it will store data upto 600 seconds


def generate_cache_key(path: str, params: dict) -> str:
    key_raw = path + json.dumps(params, sort_keys=True)
    return hashlib.sha256(key_raw.encode()).hexdigest()

# User Fetch API Start---
@router.get("/", response_model=List[Usersdata])
# @cache(expire=600)  # Automatically caches based on query parameters
async def fetch_all_users(

    skip: int = Query(0),  # Default value for skip is 0
    limit: int = Query(10000),  # Default value for limit is 10,000
    name: Optional[str] = Query(None),  # Optional filter for name
    email: Optional[str] = Query(None),  # Optional filter for email
    age: Optional[int] = Query(None),  # Optional filter for age
    db: Session = Depends(get_db)
):
    start_time = time.time()
    params = {"skip": skip, "limit": limit, "name": name, "email": email, "age": age}
    cache_key = generate_cache_key("/users", params)

    # Check cache
    cached_entry = cache.get(cache_key)

    # print(len(cached_entry),'cached data')
    # print(cached_entry,'cached_entry')
    if cached_entry:
        cached_time, cached_data = cached_entry
        if time.time() - cached_time < CACHE_TTL:
            logger.info("Returning users from cache")
            return cached_data
        else:
            # Expired - remove it
            cache.pop(cache_key)

    # No valid cache, fetch from DB
    try:
        logger.info(f"Fetching users from DB with params: {params}")
        users = get_users(db, skip=skip, limit=limit)

        # In-memory filtering
        if name:
            users = [user for user in users if name.lower() in user.name.lower()]
        if email:
            users = [user for user in users if email.lower() in user.email.lower()]
        if age:
            users = [user for user in users if user.age == age]

        # Convert SQLAlchemy models to Pydantic response
        users_data = [user.__dict__ for user in users]
        # Remove SQLAlchemy internal keys
        for user in users_data:
            user.pop('_sa_instance_state', None)

        # Save to cache with timestamp
        cache[cache_key] = (time.time(), users_data)

        cached_entry = cache.get(cache_key)

        print(len(cached_entry), 'cached data after adding')

        duration = time.time() - start_time
        logger.info(f"Fetched {len(users)} users in {duration:.3f} seconds.")
        return ORJSONResponse(content=users_data)

        # return users_data
    except Exception as e:
        logger.error(f"Error in fetch_all_users: {e}")
        raise HTTPException(status_code=500, detail="Could not fetch users")

    # cache_key = generate_cache_key("/users", params)
    # try:
    #     # # Try to get from cache
    #     # cached_result = memcache_client.get(cache_key)
    #     # print(cached_result,'cached result')
    #     # if cached_result:
    #     #     logger.info("Returning cached user data")
    #     #     return json.loads(cached_result)
    #
    #     logger.info(f"Fetching users with skip={skip}, limit={limit}, name={name}, email={email}, age={age}")
    #     users = get_users(db, skip=skip, limit=limit)
    #
    #     # Apply filters in memory
    #     if name:
    #         users = [user for user in users if name.lower() in user.name.lower()]
    #     if email:
    #         users = [user for user in users if email.lower() in user.email.lower()]
    #     if age:
    #         users = [user for user in users if user.age == age]
    #
    #     # # Convert to Pydantic models and then serialize to JSON-safe dicts
    #     # users_data = [Usersdata.from_orm(user).dict() for user in users]
    #     #
    #     # # Serialize to JSON
    #     # json_data = json.dumps(users_data, indent=2)
    #     #
    #     # # Compress the data with Gzip in memory
    #     # gzip_buffer = io.BytesIO()
    #     # with gzip.GzipFile(fileobj=gzip_buffer, mode='wb') as gz:
    #     #     gz.write(json_data.encode('utf-8'))
    #     #
    #     # # Rewind the buffer to the beginning
    #     # gzip_buffer.seek(0)
    #
    #         # Serialize for caching
    #         users_data = [user.to_dict() for user in users]  # Ensure your model has `to_dict()`
    #
    #         # Cache the result for 60 seconds
    #         memcache_client.set(cache_key, json.dumps(users_data), expire=60)
    #
    #         duration = time.time() - start_time
    #         logger.info(f"Fetched {len(users)} users in {duration:.3f} seconds.")
    #
    #         return users_data

        # Stream the gzipped file back to the client
        # return StreamingResponse(
        #     gzip_buffer,
        #     media_type="application/gzip",
        #     headers={"Content-Disposition": "attachment; filename=users.json.gz"}
        # )
        # return users
    # except Exception as e:
    #     logger.error(f"Error in fetch_all_users: {e}")
    #     raise HTTPException(status_code=500, detail="Could not fetch users")



# User Fetch API Start---
# @router.get("/", response_model=list[UserOut]) # The endpoint returns the list of users
#
# def fetch_all_users(
#     skip: int = Query(0), # records to skip **for pagination
#     limit: int = Query(10000), # number of records to return at a time
#     db: Session = Depends(get_db) # get a database session
#     ):
#
#     start_time = time.time() # the time when the fetching started
#     print("start_time",start_time)
#
#     try:
#         logger.info(f"Fetching users with skip={skip}, limit={limit}") # logging Fetch
#         users = get_users(db, skip=skip, limit=limit) # Fetch users
#         duration = time.time() - start_time # End Time
#         logger.info(f"Fetched {len(users)} users in {duration:.3f} seconds.")
#         return users
#
#     except Exception as e:
#         logger.error(f"Error in fetch_all_users: {e}") # Log errors
#
#     raise HTTPException(status_code=500, detail="Could not fetch users") # Raise HTTP 500 error for the client after getting response
# User Fetch API End---


# user_stream_cache = {}
#
# @router.get("/stream", response_class=StreamingResponse)
# async def stream_users(limit: int = Query(1000000), db: Session = Depends(get_db)) -> StreamingResponse:
#     cache_key = f"limit_{limit}"
#     logger.info(f"{cache_key} - cachekey")
#
#     # Serve from cache
#     if cache_key in user_stream_cache:
#         logger.info("Serving user stream from cache.")
#         logger.info(f"Current cache keys: {list(user_stream_cache.keys())}")
#         logger.info(f"Cached line count for {cache_key}: {len(user_stream_cache.get(cache_key, []))}")
#         return StreamingResponse(iter(user_stream_cache[cache_key]), media_type="application/json")
#
#     logger.info("Cache miss. Starting DB streaming.")
#     start_time = time.time()
#     cache_buffer = []
#
#     async def generate():
#         skip = 0
#         first_batch_time = None
#
#         while True:
#             # Sync DB call (since SQLAlchemy ORM is not async)
#             users = db.query(get_users).order_by(get_users.id).offset(skip).limit(limit).all()
#             if not users:
#                 break
#
#             if first_batch_time is None:
#                 first_batch_time = time.time()
#
#             for user in users:
#                 line = json.dumps({"id": user.id, "name": user.name}) + "\n"
#                 cache_buffer.append(line)
#                 yield line
#                 await asyncio.sleep(0)  # Yield control to event loop
#
#             skip += limit
#             logger.info(f"Streaming batch with {len(users)} users. Total streamed: {skip}")
#
#         if first_batch_time:
#             total_duration = time.time() - first_batch_time
#             logger.info(f"Streaming completed. Duration: {total_duration:.2f} seconds.")
#             user_stream_cache[cache_key] = cache_buffer
#
#     return StreamingResponse(generate(), media_type="application/json")
#

# User Fetch API end---



# -------------------------------------------practiced methods---------------------
# BATCH_SIZE = 5000
#
# def fetch_users_in_batches(db: Session, skip: int, batch_size: int) -> Generator:
#     """This function will be used to yield batches of users for streaming"""
#     while True:
#         users = get_users(db, skip=skip, limit=batch_size)
#
#         if not users:
#             break  # No more records, stop the iteration
#
#         yield users  # Yield the current batch of users
#
#         skip += batch_size  # Increment skip for next batch
#
#
# @router.get("/batch-users", response_model=list[UserOut])
# def get_users_in_batches(skip: int = Query(0), limit: int = Query(5000), db: Session = Depends(get_db)):
#     try:
#         logger.info(f"Starting to stream users with skip={skip}, limit={BATCH_SIZE}")
#
#         # Create the streaming response using the fetch_users_in_batches generator
#         return StreamingResponse(
#             fetch_users_in_batches(db, skip, BATCH_SIZE),
#             media_type="application/json"
#         )
#
#     except Exception as e:
#         logger.error(f"Error in fetching batch users: {e}")
#         raise HTTPException(status_code=500, detail="Error fetching users in batch")
#

    # ----------------------------------------------------------

# @router.get("/", response_model=list[UserOut])
#
# def list_users(
#     last_id: Optional[int] = Query(None),
#     limit: int = Query(10000),
#     db: Session = Depends(get_db)
# ) -> List[UserOut]:
#     start_time = time.time()  # Start timing the request
#     try:
#         logger.info(f"Fetching users after id={last_id}, limit={limit}")
#         users = get_users(db, last_id=last_id, limit=limit)
#         duration = time.time() - start_time  # End timing the request
#         logger.info(f"Fetched {len(users)} users in {duration:.3f} seconds")
#         return users
#     except Exception as e:
#         duration = time.time() - start_time
#         logger.error(f"Error in list_users after {duration:.3f}s: {e}")
#         raise HTTPException(status_code=500, detail="Could not fetch users")

# def list_users(skip: int = Query(0), limit: int = Query(10000), db: Session = Depends(get_db)):
#     try:
#         logger.info(f"Fetching users with skip={skip}, limit={limit}")
#         return get_users(db, skip=skip, limit=limit)
#     except Exception as e:
#         logger.error(f"Error in list_users: {e}")
#         raise HTTPException(status_code=500, detail="Could not fetch users")
# ------------------------------------------------------------------------------
#
# router = APIRouter()
# logger = logger.getLogger(__name__)
#
# BATCH_SIZE = 5000
#
# @router.get("/batch-users", response_model=list[UserOut])
# def get_users_in_batches(skip: int = Query(0), limit: int = Query(5000), db: Session = Depends(get_db)):
#     try:
#         # Initialize an empty list to collect results
#         all_users = []
#
#         while True:
#             logger.info(f"Fetching users batch: skip={skip}, limit={BATCH_SIZE}")
#             users = get_users(db, skip=skip, limit=BATCH_SIZE)
#
#             # If no users are fetched, break the loop (we've reached the end of the table)
#             if not users:
#                 logger.info("No more records found, stopping.")
#                 break
#
#             all_users.extend(users)
#
#             # Update skip for the next batch
#             skip += BATCH_SIZE
#
#         return all_users
#
#     except Exception as e:
#         logger.error(f"Error in fetching batch users: {e}")
#         raise HTTPException(status_code=500, detail="Error fetching users in batch")


# --------------------------------------------------------------------
# def stream_users(db: Session, skip: int = 0, batch_size: int = 10000):
#     while True:
#         users = get_users(db, skip=skip, limit=batch_size)
#         if not users:
#             break
#         for user in users:
#             yield json.dumps(user.dict()) + "\n"
#         skip += batch_size
#
# def stream_users_endpoint(db: Session = Depends(get_db)):
#     return responses.StreamingResponse(stream_users(db), media_type="application/json")

# @router.get("/all", response_class=responses.StreamingResponse)
# def stream_all_users(limit: int = 10000, db: Session = Depends(get_db)):
#     def user_stream():
#         skip = 0
#         while True:
#             batch = get_users(db, skip=skip, limit=limit)
#             if not batch:
#                 break
#             for user in batch:
#                 user_dict = UserOut.from_orm(user).dict()  # convert SQLAlchemy to dict
#                 yield json.dumps(user_dict) + "\n"
#             skip += limit
#
#     return responses.StreamingResponse(user_stream(), media_type="application/x-ndjson")






# ---------------------------using sream
# @router.get("/")
# def stream_users(db: Session = Depends(get_db)):
#     logger.info("Streaming of users started.")
#
#     def generate():
#         last_id = None
#         batch_count = 0
#
#         while True:
#             users = get_users(db, last_id=last_id, limit=10000)
#             if not users:
#                 logger.info(f"No more users to stream after batch {batch_count}.")
#                 break
#
#             batch_count += 1
#             logger.info(f"Streaming batch {batch_count} with {len(users)} users. last_id={last_id}")
#
#             for user in users:
#                 yield f"{user.id},{user.name}\n"
#
#             last_id = users[-1].id
#
#         logger.info("Completed streaming all user data.")
#
#     return StreamingResponse(generate(), media_type="text/plain")


# --------------------------------------------------------------------------
#
# @router.get("/", response_model=dict)
# def list_users(
#     skip: int = Query(0, ge=0),
#     limit: int = Query(100, le=10000),
#     db: Session = Depends(get_db)
# ):
#     try:
#         logger.info(f"Fetching users with skip={skip}, limit={limit}")
#         users, total = get_users_with_count(db, skip=skip, limit=limit)
#         return {
#             "total": total,
#             "skip": skip,
#             "limit": limit,
#             "data": users
#         }
#     except Exception as e:
#         logger.error(f"Error in list_users: {e}")
#         raise HTTPException(status_code=500, detail="Could not fetch users")