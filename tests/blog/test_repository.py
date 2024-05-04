import datetime as dt

import factory
import pytest
from blog.blog_post import BlogPost
from blog.repository import SqlAlchemyBlogPostRepository
from sqlalchemy.orm import Session


@pytest.fixture
def sqlalchemy_blog_post_repository(session: Session) -> SqlAlchemyBlogPostRepository:
    return SqlAlchemyBlogPostRepository(session)


class TestSqlAlchemyBlogPostRepository:
    def test_add_blog_post(
        self,
        blog_post_factory: factory.alchemy.SQLAlchemyModelFactory,
        sqlalchemy_blog_post_repository: SqlAlchemyBlogPostRepository,
        session: Session,
    ) -> None:
        expected_blog_post = blog_post_factory.build()
        sqlalchemy_blog_post_repository.add_blog_post(expected_blog_post)
        actual_blog_post = session.query(BlogPost).one()
        assert actual_blog_post == expected_blog_post

    def test_get_blog_post(
        self,
        blog_post_factory: factory.alchemy.SQLAlchemyModelFactory,
        sqlalchemy_blog_post_repository: SqlAlchemyBlogPostRepository,
    ) -> None:
        today = dt.date.today()
        yesterday = today - dt.timedelta(days=1)
        blog_post_factory.create(creation_date=yesterday)
        expected_blog_post = blog_post_factory.create(creation_date=today)
        actual_blog_post = sqlalchemy_blog_post_repository.get_blog_post(today)
        assert actual_blog_post == expected_blog_post
