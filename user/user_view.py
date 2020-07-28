from flask import Flask, request, jsonify, json, abort, Response


class UserView:
    def create_endpoint(app, services):

        user_service = services.user_service

        @app.errorhandler(400)
        def http_400_bad_request(error):
            response = jsonify({'message': error.description})
            response.status_code = 400
            return response

        @app.errorhandler(404)
        def http_404_not_found(error):
            response = jsonify({'message': error.description})
            response.status_code = 404
            return response

        @app.route("/user/signup", methods=['POST'])
        def sign_up():
            new_seller = request.json
            user_service.signup(new_seller)

            return jsonify({'message': 'SUCCESS'}, 200)
