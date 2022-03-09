import strawberry

from strawberry.types import Info


def full_name_outside_class(root: "User", info: Info) -> str:
    accessing_execution_information_info = f"context:{info.context}  variable_values:{info.variable_values}   operation:{info.operation}  path:{info.path} "
    return accessing_execution_information_info + f"{info.field_name} : {root.first_name} {root.last_name} "


@strawberry.type
class User:
    name: str
    first_name: str
    last_name: str

    # Accessing field's parent's data direct resolver
    @strawberry.field
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    # Accessing field's parent's data root
    rootparentfullname: str = strawberry.field(resolver=full_name_outside_class)


test_user = User(name="Abhinavramana", first_name="Abhinav", last_name="Ramana")


# Defining resolver separately
def get_last_user() -> User:
    return test_user


@strawberry.type
class Query:
    last_user: User = strawberry.field(resolver=get_last_user)

    @strawberry.field
    def definingResolversAsMethods(self, id: strawberry.ID) -> User:
        # here you'd use the `id` to get the user from the database
        return User(name="Abhinavbudida", first_name="Abhinav" + str(id), last_name="Budida")


schema = strawberry.Schema(query=Query)
query_string = """
    {
      lastUser {
        fullName
        name
        rootparentfullname
      }
      definingResolversAsMethods(id: 3){
        lastName
        fullName
      }
    }
    """
result = schema.execute_sync(query_string, root_value=Query())
print(result)
