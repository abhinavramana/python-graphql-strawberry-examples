import typing

import strawberry


@strawberry.type
class Audio:
    duration: int


@strawberry.type
class Video:
    thumbnail_url: str


@strawberry.type
class Image:
    src: str


@strawberry.type
class Query:
    #  to specify a name or a description for a union
    # latest_media: strawberry.union("MediaItem", types=(Audio, Video, Image))

    # latest_media: typing.Union[Audio, Video, Image]
    @strawberry.field
    def latest_media_resolving(self) -> typing.Union[Audio, Video, Image]:
        return Video(
            thumbnail_url="https://i.ytimg.com/vi/dQw4w9WgXcQ/hq720.jpg",
        )


schema = strawberry.Schema(query=Query)
query_string = """
{
    latestMediaResolving {
      ... on Audio {
        duration
      }
      ... on Video {
        thumbnailUrl
      }
      ... on Image {
        src
      }
    }
}
"""
result = schema.execute_sync(query_string, root_value=Query())
print(result)
