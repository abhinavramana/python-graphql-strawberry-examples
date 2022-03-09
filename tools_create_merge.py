import strawberry
from strawberry.tools import create_type, merge_types


@strawberry.field
def hello(info) -> str:
    print("World hello called...")
    return "World"


def get_name(info) -> str:
    print("get_name called...")
    return "info.context.user.name"

my_name = strawberry.field(name="myName", resolver=get_name)
Query = create_type("Query", [hello, my_name])
create_type_query_schema = strawberry.Schema(query=Query)
query_create_type = """{
    hello
    myName
}
"""
result = create_type_query_schema.execute_sync(query_create_type)
print(result)


@strawberry.type
class QueryA:
    @strawberry.field
    def perform_a(self) -> str:
        print("perform_a...")
        return "a"


@strawberry.type
class QueryB:
    @strawberry.field
    def perform_b(self) -> str:
        print("perform_b...")
        return "b"


ComboQuery = merge_types("ComboQuery", (QueryB, QueryA))
merge_query_schema = strawberry.Schema(query=ComboQuery)
merge_query_schema_string = """
{
  performB
  performA
}
"""
result = merge_query_schema.execute_sync(merge_query_schema_string)
print(result)
