import strawberry

from integrate_with_fast_api import get_app


@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello World"


app = get_app(Query)

# uvicorn strawberry_fastapi:app --reload
# Open http://127.0.0.1:8000/graphql
"""
{
  hello
}
"""
