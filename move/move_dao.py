from flask import abort
from datetime import datetime
import mysql.connector
import traceback


class MoveDao:
    def __init__(self, database):
        self.db_connection = database.get_connection()

    def insert_move_reservation(self, data):
        try:
            db_cursor = self.db_connection.cursor(buffered=True, dictionary=True)

            move_data = dict()
            move_data['USER_id'] = data['user_id']
            move_data['MOVE_CATEGORY_id'] = data['move_category_id']
            move_data['address'] = data['address']
            move_data['mobile_number'] = data['mobile_number']
            move_data['regist_datetime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            move_data['update_datetime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            insert_move_reservation_query = ("""
            INSERT INTO MOVE_RESERVATION (
            USER_id, MOVE_CATEGORY_id, address, mobile_number, regist_datetime, update_datetime
            ) VALUES (
            %(USER_id)s, %(MOVE_CATEGORY_id)s, %(address)s, %(mobile_number)s, %(regist_datetime)s, %(update_datetime)s
            )""")

            db_cursor.execute(insert_move_reservation_query, move_data)

            self.db_connection.commit()
            db_cursor.close()

        except KeyError as err:
            traceback.print_exc()
            abort(400, description="INVAILD_KEY")

        except mysql.connector.Error as err:
            traceback.print_exc()
            abort(400, description="INVAILD_DATA")

    def select_move_reservation(self, data):
        try:
            db_cursor = self.db_connection.cursor(buffered=True, dictionary=True)

            move_data = dict()
            move_data['USER_id'] = data['user_id']

            select_move_reservation_query = ("""
            SELECT T101.id, T102.name as move_name, T103.name as user_name, T101.address, T101.mobile_number
            FROM MOVE_RESERVATION AS T101
                INNER JOIN MOVE_CATEGORY AS T102
                        ON T102.id = T101.MOVE_CATEGORY_id
                INNER JOIN USER AS T103
                        ON T103.id = T101.USER_id
            WHERE USER_id = %(USER_id)s
            """)

            db_cursor.execute(select_move_reservation_query, move_data)
            db_result = db_cursor.fetchall()

            move_reservation_list = list()
            for row in db_result:
                dict_data = dict()
                dict_data['id'] = row['id']
                dict_data['name'] = row['user_name']
                dict_data['move_category'] = row['move_name']
                dict_data['address'] = row['address']
                dict_data['mobile_number'] = row['mobile_number']
                move_reservation_list.append(dict_data)

            self.db_connection.commit()
            db_cursor.close()

            return move_reservation_list

        except KeyError as err:
            traceback.print_exc()
            abort(400, description="INVAILD_KEY")

        except mysql.connector.Error as err:
            traceback.print_exc()
            abort(400, description="INVAILD_DATA")

    def select_move_category(self):
        try:
            db_cursor = self.db_connection.cursor(buffered=True, dictionary=True)

            select_move_category_query = ("""
            SELECT *
            FROM MOVE_CATEGORY
            """)

            db_cursor.execute(select_move_category_query)
            db_result = db_cursor.fetchall()

            move_category_list = list()
            for row in db_result:
                dict_data = dict()
                dict_data['id'] = row['id']
                dict_data['name'] = row['name']
                move_category_list.append(dict_data)

            return move_category_list

        except KeyError as err:
            traceback.print_exc()
            abort(400, description="INVAILD_KEY")

        except mysql.connector.Error as err:
            traceback.print_exc()
            abort(400, description="INVAILD_DATA")