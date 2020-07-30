from flask import abort


class HouseCleaningService:
    def __init__(self, housecleaning_dao):
        self.housecleaning_dao = housecleaning_dao

    def house_cleaning_reserve_onetime(self, data):
        try:
            insert_new_house_cleaning_reserve = self.housecleaning_dao.insert_house_cleaning_reserve(data)

            return insert_new_house_cleaning_reserve

        except KeyError:
            abort(400, description="INVALID_KEY")

    def house_cleaning_reserve_info(self, data):
        try:
            hr_reservation_list = self.housecleaning_dao.select_house_cleanning_reservation(data)

            return hr_reservation_list

        except KeyError:
            abort(400, description="INVALID_KEY")