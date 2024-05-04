from typing import Generator, Type

import factory
import pytest
from blog.blog_post import BlogPost
from blog.orm import metadata, start_mappers
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, clear_mappers, sessionmaker


@pytest.fixture
def in_memory_db() -> Engine:
    engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)
    return engine


@pytest.fixture
def session(in_memory_db: Engine) -> Generator[Session, None, None]:
    start_mappers()
    yield sessionmaker(bind=in_memory_db)()
    clear_mappers()


@pytest.fixture
def blog_post_factory(session: Session) -> Type[factory.alchemy.SQLAlchemyModelFactory]:
    class BlogPostFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = BlogPost
            sqlalchemy_session = session

        id = factory.Faker("uuid4")
        title = factory.Faker("sentence")
        content = factory.Faker("paragraph")
        creation_date = factory.Faker("date_between", start_date="-30d", end_date="now")

    return BlogPostFactory
