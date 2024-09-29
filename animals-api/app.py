from flask import Flask
from config import Config
from models.animal import db
from api.animal_api import animal_blueprint
from flasgger import Swagger

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

# Registrando o 
app.register_blueprint(animal_blueprint)
swagger = Swagger(app)
with app.app_context():
    db.create_all()


if __name__ == '__main__':
    app.run(debug=True)