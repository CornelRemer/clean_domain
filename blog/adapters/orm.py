from sqlalchemy import Column, Date, DateTime, MetaData, String, Table, text
from sqlalchemy.orm import registry

from blog.blog_post import BlogPost

metadata = MetaData()

blog_posts = Table(
    "blog_posts",
    metadata,
    Column("id", String, primary_key=True),
    Column("title", String),
    Column("content", String),
    Column("creation_date", Date, nullable=False),
    Column("created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")),
)


def start_mappers() -> None:
    registry().map_imperatively(BlogPost, blog_posts)
