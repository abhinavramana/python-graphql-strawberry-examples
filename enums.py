from enum import Enum

import strawberry


@strawberry.enum
class IceCreamFlavour(Enum):
    VANILLA = "vanilla"
    STRAWBERRY = "strawberry"
    CHOCOLATE = "chocolate"


@strawberry.type
class Cone:
    flavour: IceCreamFlavour
    num_scoops: int


@strawberry.type
class Query:

    @strawberry.field
    def best_flavour(self) -> IceCreamFlavour:
        return IceCreamFlavour.STRAWBERRY

    @strawberry.field
    def cone(self) -> Cone:
        return Cone(flavour=IceCreamFlavour.STRAWBERRY, num_scoops=4)


query_string = """
    {
      cone {
        flavour
        numScoops
      }
      bestFlavour
    }
    """

schema = strawberry.Schema(query=Query)

result = schema.execute_sync(query_string, root_value=Query())
print(result)
