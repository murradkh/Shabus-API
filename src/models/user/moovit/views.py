from flask import Blueprint, jsonify

from src.common.decorator import crossdomain
from src.models.user.moovit.errors import MoovitError
from .moovit import Moovit

moovit_blueprint = Blueprint('moovit', __name__)


@moovit_blueprint.route('', methods=['POST', 'OPTIONS'])
@crossdomain(origin='http://localhost:8100')
def moovit_user():
    try:
        Moovit.use_moovit_feature()
        return jsonify({'Status': 'Accept'})

    except MoovitError as e:
        print(e.message)
        return jsonify(Status='Reject', message=e.message)
