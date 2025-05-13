# main.py
from idlelib.debugger_r import debugging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager
from app.api.routes import users
from app.api.routes import jobs
from app.jobs import refresh_cache  # Import from your existing jobs.py

# Setup APScheduler
scheduler = BackgroundScheduler()

#
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     # Startup logic
#     scheduler.add_job(
#         refresh_cache,
#         trigger="interval",
#         seconds=1200,
#         id="refresh_user_cache",
#         replace_existing=True
#     )
#     scheduler.start()
#     print("✅ Scheduler started")
#
#     yield  # App runs here
#
#     # Shutdown logic
#     scheduler.shutdown()
#     print("🛑 Scheduler stopped")
#
# scheduler.remove_job("refresh_cache")

# app = FastAPI(lifespan=lifespan)
app = FastAPI()


# Middleware and routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/users")
app.include_router(jobs.router, prefix="/jobs")
