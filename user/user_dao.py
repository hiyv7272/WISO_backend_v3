from flask import abort
import mysql.connector


class Userdao:
    def __init__(self, database):
        self.db_connection = database.get_connection()

    def create_user(self, new_user):
        test_message = 'test_success!'
        return test_message
