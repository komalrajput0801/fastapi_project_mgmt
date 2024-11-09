from core.config import config
from fastapi import FastAPI
from user import endpoints as user_endpoints
from project import endpoints as project_endpoints

app = FastAPI(title="Project APIs", docs_url="/api-docs", debug=config.DEBUG)

app.include_router(user_endpoints.router, prefix=config.API_V1_STR)
app.include_router(project_endpoints.router, prefix=config.API_V1_STR)
