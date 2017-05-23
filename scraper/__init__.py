from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/info.db'
db = SQLAlchemy(app)
from scraper.info.views import info
app.register_blueprint(info)
db.create_all()
app.run(host='0.0.0.0')
