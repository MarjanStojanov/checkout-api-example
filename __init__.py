from flask import Flask

application = Flask(__name__)

if __name__ == 'main':
	application.run()

from app import routes
