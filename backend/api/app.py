import os
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from dependency_injector.wiring import inject, Provide
from dependency_injector import containers, providers
from core.config import Config
from .routes import  health, user,auth
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker



def init(config_file: str = os.getenv("CONFIG_FILE", ".env")) -> FastAPI:
    # Load config from .env (you can add support for .json if needed)
    config = Config(_env_file=config_file)

    # create engine and session factory
    engine = create_async_engine(config.url, echo=True, future=True)
    session_factory = async_sessionmaker(engine, expire_on_commit=False) 

    # Set up dynamic DI container
    container = containers.DynamicContainer()

    # Inject the dependencies
    container.config = providers.Object(config)
    container.engine = providers.Object(engine)
    container.session_factory = providers.Object(session_factory)

    # Create FastAPI app
    app = FastAPI(
        title="Gym Tracker API",
        version="1.0.0",
        openapi_url="/api/v1/openapi.json",
        docs_url="/api/v1/docs",
    )

    # Wire container to modules
    container.wire(modules=["db.session"])

    # attach app's container to conainter
    app.container = container
    
    # Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    v1 = APIRouter(prefix="/api/v1")
    v1.include_router(health.router)
    v1.include_router(auth.router)

    # register the v1 router
    app.include_router(v1)

    
    return app