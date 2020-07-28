from flask import request, jsonify, current_app, g, abort
from datetime import datetime, timedelta

import bcrypt
import jwt
import re



class Validate:
    def __init__(self):
        self.re_account = re.compile("^[A-Za-z0-9]+[A-Za-z0-9-_]{4,20}$")
        self.re_password = re.compile("^[A-Za-z0-9~`!@#$%\^&*()-+=]{4,}$")
        self.re_mobile_number = re.compile("^[0-9]{10,11}$")
        self.re_check_name = re.compile("^[ㄱ-ㅣ가-힣-0-9A-Za-z]([0-9ㄱ-ㅣ가-힣A-Za-z]){1,20}$")

    def check_account(self, data):
        if 'account' in data:
            if not self.re_account.match(data['account']):
                abort(400, description="INVALID_ACCOUNT")

        return None

    def check_password(self, data):
        if 'password' in data:
            if not self.re_password.match(data['password']):
                abort(400, description="INVALID_PASSWORD")

        return None

    def check_mobile_number(self, data):
        if data['mobile_number']:
            if not self.re_mobile_number.match(data['mobile_number']):
                abort(400, description="INVALID_MOBILE_NUMBER")

        return None


class UserService:
    def __init__(self, user_dao):
        self.user_dao = user_dao

    def signup(self, data):
        try:
            validate = Validate()
            validate.check_mobile_number(data)

            data['password'] = bcrypt.hashpw(data['password'].encode('UTF-8'), bcrypt.gensalt()).decode()

            insert_new_user = self.user_dao.insert_user(data)

            return insert_new_user

        except KeyError:
            abort(400, description="INVALID_KEY")

    def signin(self, data):
        try:
            # Validate.check_mobile_number(data)
            password = data['password']
            user_info = self.user_dao.select_user(data)

            if bcrypt.checkpw(password.encode('UTF-8'), user_info['password'].encode('UTF-8')):
                return user_info
            else:
                abort(400, description="INVALID_USER")

        except KeyError:
            abort(400, description="INVALID_KEY")

    def generate_access_token(self, data):
        payload = {
            'id': data['id'],
            'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)
        }
        token = jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')

        return token.decode('UTF-8')
