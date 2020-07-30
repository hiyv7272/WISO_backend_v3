from flask import abort


class MoveService:
    def __init__(self, move_dao):
        self.move_dao = move_dao

    def move_reserve(self, data):
        try:
            insert_new_user = self.move_dao.insert_move_reservation(data)

            return insert_new_user

        except KeyError:
            abort(400, description="INVALID_KEY")

    def move_reserve_info(self, data):
        try:
            move_reservation_list = self.move_dao.select_move_reservation(data)

            return move_reservation_list

        except KeyError:
            abort(400, description="INVALID_KEY")

    def move_category(self):

        move_category_list = self.move_dao.select_move_category()

        return move_category_list
