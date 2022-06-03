import logging


class BaseConfig:
    LOGGING_LEVEL = logging.INFO

    SECRET_KEY = "sadfhuhqfcjnvdf"

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456***@127.0.0.1/catalog"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ITEMS_PER_PAGE = 20
