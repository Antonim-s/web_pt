import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Application(SqlAlchemyBase):
    __tablename__ = 'application'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    sostav = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    podgotovka = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user = orm.relation('User')