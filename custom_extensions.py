import strawberry
from strawberry.extensions import Extension


class MyExtension(Extension):

    def on_request_start(self):
        print('GraphQL request start, can be asynchronously')

    def on_request_end(self):
        print('GraphQL request end, can be asynchronously')

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


schema = strawberry.Schema(query=Query, extensions=[MyExtension])
