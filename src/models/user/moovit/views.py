from flask import Blueprint, jsonify, request

from src.common.errors import CommonErrors
from src.models.user.moovit.errors import MoovitError
from .moovit import Moovit

moovit_blueprint = Blueprint('moovit', __name__)


@moovit_blueprint.route('', methods=['POST', 'OPTIONS'])
def moovit_user():
    if request.method == 'OPTIONS':
        return 'ok'
    try:
        Moovit.use_moovit_feature()
        return jsonify({'Status': 'Accept'})

    except (MoovitError, CommonErrors) as e:
        print(e.message)
        return jsonify(Status='Reject', message=e.message)
