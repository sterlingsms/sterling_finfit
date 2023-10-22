from flask import Flask
from sterling import sterling_bp
from finfit import finfit_bp
from flask_cors import CORS
import logging
from logging.handlers import RotatingFileHandler


def create_app():
	# Define WSGI object
    app = Flask(__name__)

    # Configurations
	#app.config.from_object('config')
    app.config.from_pyfile('config.py')

    # Configure logging
    log_file = 'log/finfit_app.log'
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
    handler = RotatingFileHandler(log_file, maxBytes=10000, backupCount=5)
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)
    with app.app_context():
        app.logger.addHandler(handler)
    
    # Mount the modules under /sterling and /finfit
    app.register_blueprint(sterling_bp)
    app.register_blueprint(finfit_bp)

    CORS(app, resources={r"/*": {"origins": "*"}})

	# cors = CORS(app, resources={r"/*": {"origins": ["*.sterlingadministration.com", "*.sterlingadministration.com"]}})

    return app
