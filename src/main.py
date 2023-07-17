import uvicorn
import strawberry

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from strawberry.schema.config import StrawberryConfig
from strawberry.fastapi import GraphQLRouter

from src.settings.config import settings
from src.product.query import Query


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.API_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)


if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

schema = strawberry.Schema(query=Query,config=StrawberryConfig(auto_camel_case=True))
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)