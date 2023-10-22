import sys
from os import path

# Add the app directory to the system path to import the app
sys.path.append(path.dirname(path.abspath(__file__)))
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
