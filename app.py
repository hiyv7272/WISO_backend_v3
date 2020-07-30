from flask import Flask, g
from flask_cors import CORS

import mysql.connector
import mysql.connector.pooling
from config import JWT_SECRET_KEY
from config import DATABASES
from user.user_dao import UserDao
from user.user_service import UserService
from user.user_view import UserView
from move.move_dao import MoveDao
from move.move_service import MoveService
from move.move_view import Moveview
from housecleaning.housecleaning_dao import HouseCleaningDao
from housecleaning.housecleaning_service import HouseCleaningService
from housecleaning.housecleaning_view import HouseCleaningView


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
    move_dao = MoveDao(connection_pool)
    housecleaning_dao = HouseCleaningDao(connection_pool)

    # Service layer
    services = Services
    services.user_service = UserService(user_dao)
    services.move_service = MoveService(move_dao)
    services.housecleaning_service = HouseCleaningService(housecleaning_dao)

    # Create endpoints
    UserView.create_endpoint(app, services)
    Moveview.create_endpoint(app, services)
    HouseCleaningView.create_endpoint(app, services)

    return app
