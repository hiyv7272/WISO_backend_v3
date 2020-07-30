from flask import request, jsonify, g
from utils.utils import login_decorator


class Moveview:
    def create_endpoint(app, services):
        move_service = services.move_service

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

        @app.route("/move/reserve", methods=['POST', 'GET'])
        @login_decorator
        def move_reserve():
            if request.method == 'POST':
                data = request.json
                data['user_id'] = g.user_info['id']
                move_service.move_reserve(data)

                return jsonify({'message': 'SUCCESS'})

            if request.method == 'GET':
                user_data = dict()
                user_data['user_id'] = g.user_info['id']
                move_resevation_list = move_service.move_reserve_info(user_data)

                return jsonify({'move_orders': move_resevation_list})

        @app.route("/move/category", methods=['GET'])
        def move_category():
            move_category_list = move_service.move_category()

            return jsonify({'move_category': move_category_list})