from flask import Flask, g
from flask_cors import CORS

import mysql.connector
import mysql.connector.pooling
from config import JWT_SECRET_KEY
from config import DATABASES
from user.user_dao import UserDao
from user.user_service import UserService
from user.user_view import UserView


class Services:
    pass


def make_config(app):
    app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
    return


def get_db_config():
    dbconfig = {
        'database': DATABASES['database'],
        'user': DATABASES['user'],
        'password': DATABASES['password'],
        'host': DATABASES['host'],
        'port': DATABASES['port'],
    }

    return dbconfig


def create_app(test_config=None):
    app = Flask(__name__)
    make_config(app)

    dbconfig = get_db_config()
    connection_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="mypool", pool_size=3, **dbconfig)

    CORS(app)

    # DataModel layer
    user_dao = UserDao(connection_pool)

    # Service layer
    services = Services
    services.user_service = UserService(user_dao)

    # Create endpoints
    UserView.create_endpoint(app, services)

    return app
