from flask import Flask, redirect, request
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager 

from kevin_haas_com.utils import env

config = {
    "DEBUG": True,                  # some Flask specific configs
    "CACHE_TYPE": "SimpleCache",    # Flask-Caching related configs
    "CACHE_DEFAULT_TIMEOUT": 300
}

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

app_root = env.get_app_root(__file__)
configs = env.get_configs(app_root)

DB_USERNAME = configs('DB_USERNAME')
DB_PASSWORD = configs('DB_PASSWORD')
DB_SERVER = configs('DB_SERVER')
DB_NAME = configs('DB_NAME')

app = Flask(__name__,
    static_folder='static',
    template_folder='templates')

# app.url_map.strict_slashes = False
app.config.from_mapping(config)
cache = Cache(app)

app.config['SECRET_KEY'] = DB_PASSWORD
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

#db.init_app(app)

@app.before_request
def clear_trailing():
    rp = request.path
    if rp != '/' and rp.endswith('/'):
        return redirect(rp[:-1])

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

#with app.app_context():
#    db.create_all(app=app)

#app.app_context().push()


from kevin_haas_com import routes

if __name__ == '__main__':
	app.run(
		host='0.0.0.0',
		port=5000,
		debug=True
	)
