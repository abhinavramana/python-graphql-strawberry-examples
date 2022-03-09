import asyncio
import json
from sqlite3 import Connection
from typing import Any, Dict

import strawberry
from graphql import ExecutionResult, GraphQLError
from strawberry.extensions import Extension
from strawberry.types import Info
# from mydb import get_db_session


class MyExtension(Extension):

    def on_request_start(self):
        print('GraphQL request start, can be asynchronously')
        # self.execution_context.context["db"]: Connection = get_db_session()

    def on_request_end(self):
        print('GraphQL request end, can be asynchronously')
        # self.execution_context.context["db"].close()

    # resolve can be used to run code before or after the execution of resolvers, this method must call _next with
    # all the arguments, as they will be needed by the resolvers.
    def resolve(self, _next, root, info: Info, *args, **kwargs):
        print("Asynchronouse resolve")
        return _next(root, info, *args, **kwargs)

    def get_results(self) -> Dict[str, Any]:
        print("get_results allows to return a dictionary of data or alternatively an awaitable resolving to a "
              "dictionary of data that will be included in the GraphQL response.")
        return {
            "example": "this is an example for an extension"
        }

    def on_validation_start(self):
        print('GraphQL validation start')

    def on_validation_end(self):
        print('GraphQL validation end')

    def on_parsing_start(self):
        print('GraphQL parsing start asynchronously')

    def on_parsing_end(self):
        print('GraphQL parsing end asynchronously')

    def on_executing_start(self):
        print('GraphQL execution start')

    def on_executing_end(self):
        print('GraphQL execution end')


# Use an actual cache in production so that this doesn't grow unbounded
response_cache = {}


class ExecutionCache(Extension):
    def on_executing_start(self):
        # Check if we've come across this query before
        execution_context = self.execution_context
        self.cache_key = (
            f"{execution_context.query}:{json.dumps(execution_context.variables)}"
        )
        if self.cache_key in response_cache:
            self.execution_context.result = response_cache[self.cache_key]

    def on_executing_end(self):
        execution_context = self.execution_context
        if self.cache_key not in response_cache:
            response_cache[self.cache_key] = execution_context.result


class RejectSomeQueries(Extension):
    def on_executing_start(self):
        # Reject all operations called "RejectMe"
        execution_context = self.execution_context
        if execution_context.operation_name == "RejectMe":
            self.execution_context.result = ExecutionResult(
                data=None,
                errors=[GraphQLError("Well you asked for it")],
            )


def resolve_hello(root) -> str:
    # await asyncio.sleep(1)
    return "Hello world"


@strawberry.type
class Query:
    hello: str = strawberry.field(resolver=resolve_hello)


query_string = """
{
    hello
}
"""


def run_schema(custom_extension):
    schema = strawberry.Schema(query=Query, extensions=[custom_extension])
    result = schema.execute_sync(query_string, root_value=Query())
    print(result)
    print("Ended schema run .....")


run_schema(MyExtension)
run_schema(RejectSomeQueries)
run_schema(ExecutionCache)
# schemaRejectSomeQueries = strawberry.Schema(
#     Query,
#     extensions=[
#         RejectSomeQueries,
#     ]
# )
#
# schemaExecutionCache = strawberry.Schema(
#     Query,
#     extensions=[
#         ExecutionCache,
#     ]
# )
