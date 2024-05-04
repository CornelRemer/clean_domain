import factory
from blog.blog_post import BlogPost
from sqlalchemy.orm import Session


def test_blog_post_mapper_can_save_posts(
    blog_post_factory: factory.alchemy.SQLAlchemyModelFactory, session: Session
) -> None:
    expected_blog_post = blog_post_factory.create()
    actual_blog_post = session.query(BlogPost).one()
    assert actual_blog_post == expected_blog_post
