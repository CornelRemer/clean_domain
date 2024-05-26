import factory
from blog.blog_post import BlogPost
from sqlalchemy import select
from sqlalchemy.orm import Session


def test_blog_post_mapper_can_save_posts(
    blog_post_factory: factory.alchemy.SQLAlchemyModelFactory, session: Session
) -> None:
    pass
    expected_blog_post = blog_post_factory.create()
    query = select(BlogPost)
    actual_blog_post = session.execute(query).scalars().all()
    assert actual_blog_post == [expected_blog_post]
