import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
db = SQLAlchemy(app)
auth = HTTPBasicAuth()

user_pokemon_table = db.Table(
    'user_pokemon',
    db.Column('username', db.String, db.ForeignKey('user.username')),
    db.Column('pokename', db.String, db.ForeignKey('pokemon.pokename'))
)


class User(db.Model):
    username = db.Column(db.String(255), primary_key=True)
    password_hash = db.Column(db.String(255))
    pokemons = db.relationship("Pokemon", secondary=user_pokemon_table)


class Pokemon(db.Model):
    pokename = db.Column(db.String(255), primary_key=True)


@app.route('/users')
def users():
    users = User.query.all()
    users_json = []
    for user in users:
        users_json.append({
            'username': user.username,
            'pokemons': [p.pokename for p in user.pokemons]
        })
    return jsonify(users_json)


@app.route('/pokemons')
def pokemons():
    pokemons = Pokemon.query.all()
    pokemon_json = []
    for pokemon in pokemons:
        pokemon_json.append({'pokename': pokemon.pokename})
    return jsonify(pokemon_json)


@app.route('/pokemon/add', methods=['POST'])
@auth.login_required
def pokemon_add():
    pokename = request.json.get('pokename')

    if Pokemon.query.filter(Pokemon.pokename == pokename).first():
        abort(400)

    pokemon = Pokemon(pokename=pokename)

    db.session.add(pokemon)
    db.session.commit()

    return jsonify({'pokename': pokemon.pokename})


@app.route('/user/add', methods=['POST'])
def user_add():

    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        app.logger.error('No username or password')
        abort(400)

    if User.query.filter(User.username == username).first():
        app.logger.error('The user already exists')
        abort(400)

    user = User(
        username=username, password_hash=generate_password_hash(password)
        )

    db.session.add(user)
    db.session.commit()
    return jsonify({'username': user.username})


@auth.verify_password
def verify_password(username, password):

    user = User.query.filter(User.username == username).first()

    if not user:
        return None

    if check_password_hash(user.password_hash, password):

        return user


@app.route('/pokemon/choose', methods=['POST'])
@auth.login_required
def pokemon_choose():
    pokenames = request.json
    user = auth.current_user()
    pokemons = []
    for pokename in pokenames:
        pokemon = Pokemon.query.filter(Pokemon.pokename == pokename).first()
        if not pokemon:
            abort(400)
        pokemons.append(pokemon)

    user.pokemons = pokemons

    db.session.add(user)
    db.session.commit()
    return jsonify({'username': user.username, 'pokemons': [p.pokename for p in user.pokemons]})
