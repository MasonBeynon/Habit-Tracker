from fastapi import FastAPI
from .routes import router
from .database import engine, Base

app = FastAPI()

app.include_router(router)

import asyncio
from sqlalchemy.exc import OperationalError

@app.on_event("startup")
async def startup():
    for _ in range(10):  # Retry up to 10 times
        try:
            async with engine.begin() as conn:
                # Optional: run migrations or test a simple query
                print("✅ Database connection successful.")
                break
        except OperationalError:
            print("❌ Database not ready. Retrying...")
            await asyncio.sleep(2)
    else:
        print("❌ Database connection failed after retries.")
        raise RuntimeError("Database is not available.")