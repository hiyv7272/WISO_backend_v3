from flask import request, jsonify, json, abort, Response


class UserView:
    def create_endpoint(app, services):
        user_service = services.user_service

        @app.errorhandler(400)
        def http_400_bad_request(error):
            response = jsonify({'message': error.description})
            response.status_code = 400
            return response

        @app.errorhandler(401)
        def http_401_unauthorized(error):
            response = jsonify({'message': error.description})
            response.status_code = 401
            return response

        @app.errorhandler(404)
        def http_404_not_found(error):
            response = jsonify({'message': error.description})
            response.status_code = 404
            return response

        @app.route("/user/signup", methods=['POST'])
        def sign_up():
            data = request.json
            user_service.signup(data)

            return jsonify({'message': 'SUCCESS'})

        @app.route("/user/signin", methods=['POST'])
        def sign_in():
            try:
                data = request.json
                user_info = user_service.signin(data)
                token = user_service.generate_access_token(user_info)

                return jsonify({'access_token': token})

            except:
                abort(401, description='http_401_unauthorized')
