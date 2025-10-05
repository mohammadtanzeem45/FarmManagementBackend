from flask import Flask
from models import db
from routes import create_routes

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

create_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
