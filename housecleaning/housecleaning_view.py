from flask import request, jsonify, g
from utils.utils import login_decorator


class HouseCleaningView:
    def create_endpoint(app, services):
        housecleaning_service = services.housecleaning_service

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

        @app.route("/housecleaning/reserve/onetime", methods=['POST'])
        @login_decorator
        def house_cleaning_reserve():
            data = request.json
            data['user_id'] = g.user_info['id']
            housecleaning_service.house_cleaning_reserve_onetime(data)

            return jsonify({'message': 'SUCCESS'})

        @app.route("/housecleaning/reserve", methods=['GET'])
        @login_decorator
        def house_cleaning_reserve_info():
            data = dict()
            data['user_id'] = g.user_info['id']
            house_cleaning_reserve_list = housecleaning_service.house_cleaning_reserve_info(data)

            return jsonify({'move_orders': house_cleaning_reserve_list})