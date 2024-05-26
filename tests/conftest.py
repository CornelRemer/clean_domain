from typing import Generator, Type

import factory
import pytest
from blog.adapters.orm import metadata, start_mappers
from blog.blog_post import BlogPost
from sqlalchemy import Engine
from sqlalchemy.orm import Session, clear_mappers, sessionmaker

from tests.helper import DatabaseManager, DBSettings


@pytest.fixture
def postgres_engine() -> Generator[Engine, None, None]:
    db_manager = DatabaseManager(settings=DBSettings.from_env())
    with db_manager.database("test_db") as db_url:
        with db_manager.engine(db_url) as engine:
            metadata.create_all(engine)
            yield engine


@pytest.fixture
def session(postgres_engine: Engine) -> Generator[Session, None, None]:
    connection = postgres_engine.connect()
    session = sessionmaker(bind=connection)()
    start_mappers()
    try:
        yield session
    finally:
        session.close()
        connection.close()
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
