from flask import abort
from datetime import datetime
import mysql.connector
import traceback


class HouseCleaningDao:
    def __init__(self, database):
        self.db_connection = database.get_connection()