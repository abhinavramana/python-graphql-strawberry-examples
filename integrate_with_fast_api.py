import strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter


def get_app(queryType):
    """
    # uvicorn FILENAME:app --reload
    # Open http://127.0.0.1:8000/graphql
    """
    strawberry_schema = strawberry.Schema(query=queryType)
    graphql_app = GraphQLRouter(strawberry_schema)
    app = FastAPI()
    app.include_router(graphql_app, prefix="/graphql")
    return app
