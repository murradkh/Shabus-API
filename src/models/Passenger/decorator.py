# from functools import wraps
# from flask import request, jsonify
# from src.Common.Utilites import Utils
#
# def valid_token_exist(f):
#     @wraps(f)
#     def decorated_function():
#         content = request.get_json()
#         token = content.get('Token')
#         valid = Utils.Token_Isvalid(token)
#         if valid is False:
#             print('token is not valid!')
#             return jsonify({'Status': 'Reject', 'message': 'UnAuthorized Access!'})
#
#         print(token)
#         # return jsonify({'Status': 'Accept', 'message': 'The Ride is recorded!'})
#         return f(token)
#     return decorated_function
