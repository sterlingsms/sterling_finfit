from flask import Flask, jsonify, make_response
from werkzeug.exceptions import HTTPException

app = Flask(__name__)

class APIException(HTTPException):
    status_code = None
    message = None
    payload = None
  
    def __init__(self, message, status_code=None, payload=None):
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        if payload is not None:
            self.payload = payload
      
    @property
    def response(self):
        response = jsonify({'error': self.message})
        response.status_code = self.status_code
        return response
        
    def to_dict(self):
        res = dict(self.payload or ())
        res['error'] = self.message
        return res

@app.errorhandler(APIException)
def handle_api_exception(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
    #return make_response(jsonify(error.to_dict()), error.status_code)

@app.errorhandler(404)
def handle_not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)