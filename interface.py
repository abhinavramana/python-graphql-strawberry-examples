import typing

import strawberry


@strawberry.interface
class Customer:
    raw_name: str

    # An interface has fields, but it’s never instantiated.
    @strawberry.field
    def name(self) -> str:
        return self.raw_name.title()


@strawberry.type
class Individual(Customer):
    employed_by = None  # employed_by: typing.Optional["Company"] = None


@strawberry.type
class Company(Customer):
    employees: typing.List[Individual]

    @strawberry.field
    def name(self) -> str:
        return f"{self.raw_name} Limited"


@strawberry.type
class Query:
    @strawberry.field
    def best_customers(self) -> typing.List[Customer]:
        i1 = Individual(raw_name="abhinav")
        i2 = Individual(raw_name="vivek")
        c = Company(raw_name="wombo", employees=[i1, i2])
        i1.employed_by = c
        return [i2, c]


query_string = """
    {
      bestCustomers {
        name
      }
    }
    """

schema = strawberry.Schema(query=Query, types=[Individual, Company])
result = schema.execute_sync(query_string, root_value=Query())
print(result)
