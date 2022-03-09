import strawberry

from strawberry.schema.config import StrawberryConfig

def bakvas() :
    return "omg"
@strawberry.type
class Query:
    example_field: str = strawberry.field(resolver=bakvas)


schema = strawberry.Schema(
    query=Query, config=StrawberryConfig(auto_camel_case=False)
)