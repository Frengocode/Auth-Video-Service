from fastapi import FastAPI
from src.services.user_service.api import user_service_router
from src.services.auth_service.api import auth_service
from fastapi.middleware.cors import CORSMiddleware
from src.core.databse import Base, engine


app = FastAPI(title="User And Auth Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



@app.on_event("startup")
async def on_startup():
    await create_tables()


app.include_router(user_service_router)
app.include_router(auth_service)
