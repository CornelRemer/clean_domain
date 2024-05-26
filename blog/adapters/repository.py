import datetime as dt
from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from blog.blog_post import BlogPost


class AbstractBlogPostRepository(ABC):
    @abstractmethod
    def add_blog_post(self, blog_post: BlogPost) -> None:
        pass

    @abstractmethod
    def get_blog_post(self, creation_date: dt.date) -> BlogPost | None:
        pass


class SqlAlchemyBlogPostRepository(AbstractBlogPostRepository):
    def __init__(self, session: Session) -> None:
        self._session = session

    def add_blog_post(self, blog_post: BlogPost) -> None:
        self._session.add(blog_post)

    def get_blog_post(self, creation_date: dt.date) -> BlogPost | None:
        return self._session.query(BlogPost).filter_by(creation_date=creation_date).first()
