from flask import abort
from datetime import datetime
import mysql.connector
import traceback


class UserDao:
    def __init__(self, database):
        self.db_connection = database.get_connection()

    def insert_user(self, data):
        try:
            db_cursor = self.db_connection.cursor(buffered=True, dictionary=True)

            user_data = dict()
            user_data['email'] = data['email']
            user_data['name'] = data['name']
            user_data['password'] = data['password']
            user_data['mobile_number'] = data['mobile_number']
            user_data['regist_datetime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            user_data['update_datetime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            insert_user_data = ("""
                                INSERT INTO USER (
                                email, name, password, mobile_number, regist_datetime, update_datetime
                                ) VALUES (
                                %(email)s, %(name)s, %(password)s, %(mobile_number)s, %(regist_datetime)s, %(update_datetime)s
                                )""")

            db_cursor.execute(insert_user_data, user_data)

            self.db_connection.commit()
            db_cursor.close()

        except KeyError as err:
            traceback.print_exc()
            abort(400, description="INVAILD_KEY")

        except mysql.connector.Error as err:
            traceback.print_exc()
            abort(400, description="INVAILD_DATA")

    def select_user(self, data):
        try:
            db_cursor = self.db_connection.cursor(buffered=True, dictionary=True)

            user_data = dict()
            user_data['email'] = data['email']

            select_user_data = ("""
                                SELECT id, email, password
                                FROM USER
                                WHERE email = %(email)s
                                """)

            db_cursor.execute(select_user_data, user_data)
            user_info = dict()
            for row in db_cursor:
                user_info['id'] = row['id']
                user_info['email'] = row['email']
                user_info['password'] = row['password']

            self.db_connection.commit()
            db_cursor.close()

            return user_info

        except KeyError as err:
            traceback.print_exc()
            abort(400, description="INVAILD_KEY")

        except mysql.connector.Error as err:
            traceback.print_exc()
            abort(400, description="INVAILD_DATA")