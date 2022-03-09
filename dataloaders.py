from typing import List, Union, Any, Optional

import strawberry
from strawberry.types import Info
from strawberry.asgi import GraphQL
from strawberry.dataloader import DataLoader

from starlette.requests import Request
from starlette.websockets import WebSocket
from starlette.responses import Response
import asyncio


@strawberry.type
class User:
    # first we need to define a function that allows to fetch data in batches
    id: strawberry.ID


# would interact with a database or 3rd party API
async def load_users_database(keys: List[int]) -> List[User]:
    x = []
    for key in keys:
        user_created = create_user(key)
        y = await user_created
        x.append(y)
    return x


async def create_user(userid: int, wait=3) -> User:
    print(f"Creating User {userid} for {wait} seconds... ")
    await asyncio.sleep(wait)
    print(f"Created User {userid}")
    return User(id=userid)


loader = DataLoader(load_fn=load_users_database)

"""the dataloader is instantiated outside the resolver, since we need to share it between multiple resolvers or even 
between multiple resolver calls. However this is a not a recommended pattern when using your schema inside a server 
because the dataloader will so cache results for as long as the server is running. dataloader when creating the 
GraphQL context so that it only caches results with a single request. """


class MyGraphQL(GraphQL):
    async def get_context(self, request: Union[Request, WebSocket], response: Optional[Response]) -> Any:
        return {
            "user_loader": DataLoader(load_fn=load_users_database)
        }


@strawberry.type
class Query:
    @strawberry.field
    async def get_user(self, info: Info, id: strawberry.ID) -> User:
        return await info.context["user_loader"].load(id)


schema = strawberry.Schema(query=Query)
query_string = """
{
  first: getUser(id: 1) {
    id
  }
  second: getUser(id: 2) {
    id
  }
}"""
app = MyGraphQL(schema)


# pip install uvicorn
# uvicorn dataloaders:app


async def main():
    print("Single user 1")
    user = await loader.load(1)
    print("User 2,3 in parallel by gather...")
    [user_a, user_b] = await asyncio.gather(loader.load(2), loader.load(3))

    # by default DataLoader caches the loads:
    print("Single user 1, cache checking")
    await loader.load(1)
    await loader.load(1)
    print("User 4,5,6 in parallel by load_many")
    [user_c, user_d, user_e] = await loader.load_many([4, 5, 6])

# asyncio.run() cannot be called from a running event loop when using uvicorn
# asyncio.run(main())
