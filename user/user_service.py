import bcrypt
import jwt

from flask import request, jsonify, current_app, g, abort


class UserService:
    def __init__(self, user_dao):
        self.user_dao = user_dao

    def signup(self, new_user):
        try:
            # validation = self.validate(new_seller)
            # new_user['password'] = bcrypt.hashpw(
            #     new_user['password'].encode('UTF-8'),
            #     bcrypt.gensalt()
            # )

            create_new_user = self.user_dao.create_user(new_user)

            return create_new_user

        except KeyError:
            abort(400, description="INVALID_KEY")

    # """
    # 로그인_체크 메소드
    # """
    #
    # def signin(self, user_data):
    #     try:
    #         validation = self.validate(user_data)
    #         password = user_data['password']
    #         user_info = self.seller_dao.get_user_info(user_data)
    #
    #         if bcrypt.checkpw(password.encode('UTF-8'), user_info['password'].encode('UTF-8')):
    #             return user_info
    #         else:
    #             abort(400, description="INVALID_USER")
    #
    #     except KeyError:
    #         abort(400, description="INVALID_KEY")
    #
    # """
    # access_token(JWT) 생성 메소드
    # """
    #
    # def generate_access_token(self, user_info):
    #     payload = {
    #         'accounts_id': user_info['id'],
    #         'authorities_id': user_info['authorities_id'],
    #         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)
    #     }
    #     token = jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], 'HS256')
    #
    #     return token.decode('UTF-8')
