import typing
import strawberry

from integrate_with_fast_api import get_app


@strawberry.type
class Book:  # Object types
    title: str  # Scalar types
    author_name: str


# Object types can refer to each other, as we had in our schema earlier:
@strawberry.type
class Author:
    name: str  # Scalar types
    books_written: typing.List['Book']


def get_books():
    return [
        Book(
            title='The Great Gatsby',
            author_name='Abhinav',
        ),
    ]


def get_authors():
    return [
        Author(
            name='Abhinav',
            books_written=get_books(),
        ),
    ]


@strawberry.type
class Query:
    """
    The Query type defines exactly which GraphQL queries (i.e., read operations) clients can execute against your
    data. It resembles an object type, but its name is always Query. """
    # This Query type defines two available queries: books and authors. Each query returns a list
    # of the corresponding type.
    books: typing.List[Book] = strawberry.field(resolver=get_books)
    authors: typing.List[Author] = strawberry.field(resolver=get_authors)
    """ 
    query {
      books {
        title
      }
      authors {
        name
        booksWritten {
          title
        }
      }
    }
    """

@strawberry.input
class AddBookInput:
  title: str = strawberry.field(description="The title of the book")
  author: str = strawberry.field(description="The name of the author")

@strawberry.type
class Mutation:
    @strawberry.field
    # Strawberry converts fields names from snake case to camel case automatically.
    def add_book(self, title: str, author: str) -> Book:
        return Book(title=title, author_name=author)
        """
        mutation {
          addBook(title: "Fox in Socks", author: "Dr. Seuss") {
            title
            authorName
          }
        }
        """

    #Input types - BUGGY!
    @strawberry.field
    def add_book_input_type(self, book: AddBookInput) -> Book:
        return Book(title=book.title, author=book.author)


# app = get_app(Query)
schema = strawberry.Schema(query=Query, mutation=Mutation)
# Run: strawberry server schema_basics
