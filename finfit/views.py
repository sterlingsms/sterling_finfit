from flask import jsonify, request, Response
from . import finfit_bp
from .controllers import get_org_data
import urllib
import urllib.parse
from APIException import APIException

@finfit_bp.route('/org_chart', methods=['GET'])
@finfit_bp.route('/org_chart/', methods=['GET'])
def order_collection_data():
	# print(request.path)
    parsed_url = urllib.parse.urlparse(request.url)
    if request.args.get("rid"):
        rid = urllib.parse.parse_qs(parsed_url.query).get('rid')[0]
        data = get_org_data(rid)
        return jsonify(data)
    else:
    	raise APIException('Invalid request - Query parameter rid is missing', status_code=400)
