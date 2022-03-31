import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("postgresql://recipes_flask:pass_flask@db:5432/recipes_flask", "sqlite://")
