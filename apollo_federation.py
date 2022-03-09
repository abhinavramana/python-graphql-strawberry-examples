from typing import List, Optional

import strawberry


@strawberry.federation.type(keys=["id"])
# Federation keys can be thought of as primary keys. They are used by the gateway to query types between multiple
# services and then join them into the augmented type.
# Here, we are telling the federation system that the Book's id field is its uniquely-identifying key.
class Book:
    id: strawberry.ID
    title: str


def get_all_books() -> List[Book]:
    return [Book(id=1, title="The Dark Tower")]


@strawberry.type
class Query:
    all_books: List[Book] = strawberry.field(resolver=get_all_books)


base_query = """
{
    allBooks {
        id
        title
    }
}"""
base_schema = strawberry.federation.Schema(query=Query)
result = base_schema.execute_sync(base_query, root_value=Query())
print(result)


# ========= we want to define a type for a review but also extend the Book type to have a list of reviews.========
@strawberry.type
class Review:
    id: int
    body: str


def get_reviews(root: "Book") -> List[Review]:
    return [
        Review(id=id_, body=f"A review for {root.id}")
        for id_ in range(root.reviews_count)
    ]


@strawberry.federation.type(extend=True, keys=["id"])
# extend the Book type by using again strawberry.federation.type because we need to tell federation that we are
# extending a type that already exists, not creating a new one.
class Book:
    id: strawberry.ID = strawberry.federation.field(external=True)  # tells federation that this field is not
    # available in this service, and that it comes from another service.
    reviews_count: int
    reviews: List[Review] = strawberry.field(resolver=get_reviews)

    @classmethod
    def resolve_reference(cls, id: strawberry.ID):
        # here we could fetch the book from the database allows us to instantiate types when they are referred to by
        # other services. Called when a GraphQL operation references an entity across multiple services
        return Book(id=id, reviews_count=3)


@strawberry.type
# define a Query type, even if our service only has one type that is not used directly in any GraphQL query. This is
# because the GraphQL spec mandates that a GraphQL server defines a Query type, even if it ends up being empty/unused
class Query:
    _service: Optional[str]


# Since they are not reachable from the Query field itself, Strawberry won't be able to find them by default.
schema = strawberry.federation.Schema(query=Query, types=[Book, Review])
# ========== GATEWAY =================
"""
const { ApolloServer } = require("apollo-server");
const { ApolloGateway } = require("@apollo/gateway");

const gateway = new ApolloGateway({
  serviceList: [
    { name: "books", url: "http://localhost:8000" },
    { name: "reviews", url: "http://localhost:8080" },
  ],
});

const server = new ApolloServer({ gateway });

server.listen().then(({ url }) => {
  console.log(`🚀 Server ready at ${url}`);
});
"""
# https://github.com/strawberry-graphql/federation-demo/blob/main/gateway/server.ts

q = """{
  # query defined in the books service
  books {
    id
    reviewsCount
    # field defined in the reviews service
    reviews {
      body
    }
  }
}
"""
