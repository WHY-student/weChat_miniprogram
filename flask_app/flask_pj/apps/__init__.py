import os
from flask import Flask
from .flask_pj import init_blue_print
from .utils import config_log
from flask_pj.config import config
from flask_mongoengine import MongoEngine
import sys
from flask_cors import CORS
# sys.path.append("flask_pj/model")
# import model
from flask_apscheduler import APScheduler

scheduler = APScheduler()

db = MongoEngine()


def override_json_encoder(app: Flask):
    from bson import ObjectId
    from datetime import date

    superclass = app.json_encoder

    class _JsonEncoder(superclass):
        def default(self, o):
            if isinstance(o, ObjectId):
                return str(o)
            if isinstance(o, date):
                return o.isoformat()
            return superclass.default(self, o)

    app.json_encoder = _JsonEncoder


def create_app():
    config_log()
    app = Flask(__name__, static_folder='static', static_url_path='')
    CORS(app, supports_credentials=True)
    env = os.environ.get('FLASK_ENV', 'default')
    app.config.from_object(config.get(env))
    init_blue_print(app)
    # 通过MONGODB_SETTINGS配置MongoEngine
    app.config['MONGODB_SETTINGS'] = {
        'db': 'hello',
        'host': '159.75.23.139',
        'port': 27017,
        'connect': True
    }
    db.init_app(app)
    scheduler.start()

    return app

