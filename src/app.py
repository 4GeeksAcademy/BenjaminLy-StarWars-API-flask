"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planet, Character
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def get_users():
    users = User.query.all()
    all_user = list(map( lambda x : x.serialize() , users ))
    return jsonify(all_user), 200

@app.route('/user/favorites', methods=['GET'])
def get_user_favorites():
    favorites_list= Favorites.query.all()
    favorites_serialize = [item.serialize() for item in favorites_list]
    return jsonify(favorites_serialize), 200

# character endpoints
@app.route('/character', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    all_characters = list(map( lambda x : x.serialize() , characters ))
    return jsonify(all_characters), 200

@app.route('/characters/<int:characters_id>', methods=['GET'])
def get_characters_id(Character_id):
    characters = Character.query.filter_by(id = Character_id).first()
    return jsonify(characters.serialize()), 200

@app.route('/favorites/character/<int:character_id>', methods=['POST'])
def add_character_favorite(character_id):
    user_id = request.json.get('user_id')
    user = User.query.filter_by(id = user_id).first()
    if user is None:
        return 'User does not exist', 404
    character = Character.query.filter_by(id = character_id).first()
    if character is None:
        return 'Character does not exist', 404
    if user.favorite_characters is None:
        user.favorite_characters = []
    if character in user.favorite_characters:
        return 'This is character is already in favorites'
    user.favorite_characters.append(character)
    payload = {
        'msg' : 'Congrats favorite successfully saved',
        'user' : user.serialize()
    }
    return jsonify(payload), 200

@app.route('/favorites/character/<int:character_id>', methods=['DELETE'])
def delete_character_favorite(character_id):
    user_id = request.json.get('user_id')
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return 'User does not exist', 404
    character = Character.query.filter_by(id=character_id).first()
    if character is None:
        return 'Character does not exist', 404
    if character in user.favorite_characters:
        user.favorite_characters.remove(character)
        db.session.commit()
        return 'Character removed from favorites', 200
    else:
        return 'Character is not in favorites', 404

# planet endpoints

@app.route('/planet', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    all_planets = list(map( lambda x : x.serialize() , planets ))
    return jsonify(all_planets), 200

@app.route('/planet/<int:planets_id>', methods=['GET'])
def get_planets_id(Planet_id):
    planets = Planet.query.filter_by(id = Planet_id).first()
    return jsonify(planets.serialize()), 200

@app.route('/favorites/planet/<int:planet_id>', methods=['POST'])
def add_planet_favorite(planet_id):
    user_id = request.json.get('user_id')
    user = User.query.filter_by(id = user_id).first()
    if user is None:
        return 'User does not exist', 404
    planet = Planet.query.filter_by(id = planet_id).first()
    if planet is None:
        return 'Planet does not exist', 404
    if user.favorite_planets is None:
        user.favorite_planets = []
    if planet in user.favorite_planets:
        return 'This is planet is already in favorites'
    user.favorite_planets.append(planet)
    payload = {
        'msg' : 'Congrats favorite successfully saved',
        'user' : user.serialize()
    }
    return jsonify(payload), 200
    
@app.route('/favorites/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet_favorite(planet_id):
    user_id = request.json.get('user_id')
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return 'User does not exist', 404
    planet = Planet.query.filter_by(id=planet_id).first()
    if planet is None:
        return 'Planet does not exist', 404
    if planet in user.favorite_planets:
        user.favorite_planets.remove(planet)
        db.session.commit()
        return 'Planet removed from favorites', 200
    else:
        return 'Planet is not in favorites', 404


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
