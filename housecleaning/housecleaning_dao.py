from flask import abort
from datetime import datetime
import mysql.connector
import traceback


class HouseCleaningDao:
    def __init__(self, database):
        self.db_connection = database.get_connection()

    def insert_house_cleaning_reserve(self, data):
        try:
            db_cursor = self.db_connection.cursor(buffered=True, dictionary=True)

            house_cleaning_data = dict()
            house_cleaning_data['USER_id'] = data['user_id']
            house_cleaning_data['RESERVE_CYCLE_id'] = data['reserve_cycle_id']
            house_cleaning_data['service_start_date'] = data['service_start_date']
            house_cleaning_data['SERVICE_DURATION_id'] = data['service_duration_id']
            house_cleaning_data['SERVICE_STARTING_TIME_id'] = data['service_starting_time_id']
            house_cleaning_data['reserve_location'] = data['reserve_location']
            house_cleaning_data['have_pet'] = data['have_pet']
            house_cleaning_data['STATUS_id'] = 1
            house_cleaning_data['regist_datetime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            house_cleaning_data['update_datetime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            insert_house_cleanning_reservation = ("""
            INSERT INTO HOUSECLEANING_RESERVATION (
            USER_id, RESERVE_CYCLE_id, service_start_date, SERVICE_DURATION_id, SERVICE_STARTING_TIME_id, reserve_location, have_pet, STATUS_id, regist_datetime, update_datetime
            ) VALUES (
            %(USER_id)s, %(RESERVE_CYCLE_id)s, %(service_start_date)s, %(SERVICE_DURATION_id)s, %(SERVICE_STARTING_TIME_id)s, %(reserve_location)s, %(have_pet)s, %(STATUS_id)s, %(regist_datetime)s, %(update_datetime)s
            )""")

            db_cursor.execute(insert_house_cleanning_reservation, house_cleaning_data)

            self.db_connection.commit()
            db_cursor.close()

        except KeyError as err:
            traceback.print_exc()
            abort(400, description="INVAILD_KEY")

        except mysql.connector.Error as err:
            traceback.print_exc()
            abort(400, description="INVAILD_DATA")

    def select_house_cleanning_reservation(self, data):
        try:
            db_cursor = self.db_connection.cursor(buffered=True, dictionary=True)

            hr_data = dict()
            hr_data['USER_id'] = data['user_id']

            select_hr_reservation_query = ("""
            SELECT T101.id, T102.name, T103.reserve_cycle, T104.service_duration, T105.starting_time, T101.service_start_date, T101.reserve_location, T101.have_pet, T106.status
            FROM HOUSECLEANING_RESERVATION AS T101
                INNER JOIN USER AS T102
                        ON T102.id = T101.USER_id
                INNER JOIN RESERVE_CYCLE AS T103
                        ON T103.id = T101.RESERVE_CYCLE_id
                INNER JOIN SERVICE_DURATION AS T104
                        ON T104.id = T101.SERVICE_DURATION_id
                INNER JOIN SERVICE_STARTING_TIME AS T105
                        ON T105.id = T101.SERVICE_STARTING_TIME_id
                INNER JOIN STATUS AS T106
                        ON T106.id = T101.STATUS_id 
            WHERE USER_id = %(USER_id)s
            """)

            db_cursor.execute(select_hr_reservation_query, hr_data)
            db_result = db_cursor.fetchall()

            hr_reservation_list = list()
            for row in db_result:
                dict_data = dict()
                dict_data['id'] = row['id']
                dict_data['name'] = row['name']
                dict_data['reserve_cycle'] = row['reserve_cycle']
                dict_data['service_duration'] = row['service_duration']
                dict_data['starting_time'] = row['starting_time']
                dict_data['service_start_date'] = row['service_start_date']
                dict_data['reserve_location'] = row['reserve_location']
                dict_data['have_pet'] = row['have_pet']
                dict_data['status'] = row['status']
                hr_reservation_list.append(dict_data)

            self.db_connection.commit()
            db_cursor.close()

            return hr_reservation_list

        except KeyError as err:
            traceback.print_exc()
            abort(400, description="INVAILD_KEY")

        except mysql.connector.Error as err:
            traceback.print_exc()
            abort(400, description="INVAILD_DATA")