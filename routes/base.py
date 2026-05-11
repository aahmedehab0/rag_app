from fastapi import APIRouter
import os
base_router = APIRouter(
    prefix= "/rag",
    tags= ["api_v1"]
    )

@base_router.get("/welcome")

async def welcome():
    app_name = os.getenv("App_name")
    app_version = os.getenv("App_version")
    return{
        "App name": app_name,
        "App Version" : app_version
    }