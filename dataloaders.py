import asyncio

import strawberry
from typing import List
from strawberry.dataloader import DataLoader


@strawberry.type
# first we need to define a function that allows to fetch data in batches
class User:
    id: strawberry.ID


# would interact with a database or 3rd party API
async def load_users(keys: List[int]) -> List[User]:
    x = []
    for key in keys:
        user_created = create_user(key)
        y = await user_created
        x.append(y)
    return x


async def create_user(userid: int, wait=4) -> User:
    print(f"Creating User {userid} for {wait} seconds... ")
    await asyncio.sleep(wait)
    print(f"Created User {userid}")
    return User(id=userid)


loader = DataLoader(load_fn=load_users)


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


asyncio.run(main())
