import random
import typing
from typing import Optional
import strawberry


@strawberry.type
class User:
    name: str

    def __hash__(self):
        return hash(self.name)


def get_user_by_email() -> User:
    raise ValueError("get_user_by_email")


@strawberry.type
class QueryForOptionalResults:
    @strawberry.field
    # making the field optional when there is a possibility that the data won’t exist
    def get_user(self) -> Optional[User]:
        try:
            user = get_user_by_email()
            return user
        except ValueError:
            return None


query_string_for_optional = """{
  getUser {
    name
  }
}"""
schema = strawberry.Schema(query=QueryForOptionalResults)
result = schema.execute_sync(query_string_for_optional)
print(result)


@strawberry.type
class RegisterUserSuccess:
    user: User


@strawberry.type
class UsernameAlreadyExistsError:
    username: str
    alternative_username: str


# Create a Union type to represent the 2 results from the mutation
Response = strawberry.union(
    "RegisterUserResponse",
    [RegisterUserSuccess, UsernameAlreadyExistsError]
)

user_db = {}
abhinav = User("abhinav")
user_db[abhinav] = "password"


def username_already_exists(username):
    return username in user_db


def generate_username_suggestion(username):
    number = '{:03d}'.format(random.randrange(1, 999))
    return username + number


def create_user(username, password):
    user = User(username)
    user_db[user] = password
    return user


@strawberry.type
class Mutation:
    @strawberry.mutation
    def register_user(self, username: str, password: str) -> Response:
        if username_already_exists(username):
            return UsernameAlreadyExistsError(
                username=username,
                alternative_username=generate_username_suggestion(username)
            )

        user = create_user(username, password)
        return RegisterUserSuccess(
            user=user
        )


query_mutation_register_success = """mutation {
    registerUser(username: "Fox in Socks", password: "Dr. Seuss") {
        user {
            name
        }
      }
    }"""
q = """
mutation RegisterUser($username: String!, $password: String!) {
  registerUser(username: $username, password: $password) {
    __typename
    ... on UsernameAlreadyExistsError {
      alternativeUsername
    }
    ... on RegisterUserSuccess {
      id
      username
    }
  }
}"""
query_mutation_register_failure = """mutation {
    registerUser(username: "abhinav", password: "lol") {
        username
        alternativeUsername
      }
    }"""
schemaRegisterUser = strawberry.Schema(mutation=Mutation, query=QueryForOptionalResults)
result = schema.execute_sync(q)
print(result)
