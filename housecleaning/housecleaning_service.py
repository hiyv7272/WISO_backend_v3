from flask import abort


class HouseCleaningService:
    def __init__(self, housecleaning_dao):
        self.housecleaning_dao = housecleaning_dao

    def house_cleaning_reserve_onetime(self, data):
        pass
    # def move_reserve(self, data):
    #     try:
    #         insert_new_user = self.move_dao.insert_move_reservation(data)
    #
    #         return insert_new_user
    #
    #     except KeyError:
    #         abort(400, description="INVALID_KEY")