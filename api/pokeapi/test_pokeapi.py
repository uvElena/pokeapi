import base64
from flask_testing import TestCase
from .app import app, db, User, Pokemon
from sqlalchemy.exc import OperationalError
from time import sleep


class TestPokeApi(TestCase):

    def create_app(self):
        return app

    def setUp(self):
        while True:
            try:
                db.drop_all()
                break
            except OperationalError:
                print("Oops! Database is not available. Try again...")
                sleep(5)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_user_add(self):
        self.client.post(
            '/user/add',
            json={'username': 'user1', 'password': '1234'},
        )

        user = User.query.filter(User.username == 'user1').first()
        self.assertNotEqual(user, None)

        response = self.client.get('users')
        self.assertEqual(response.json[0]['username'], 'user1')

    def test_pokemon_add(self):
        self.client.post(
            '/user/add',
            json={'username': 'user1', 'password': '1234'},
        )
        credentials = base64.b64encode(b'user1:1234').decode('utf-8')

        self.client.post(
            '/pokemon/add',
            json={'pokename': 'pokemon1'},
            headers={'Authorization': 'Basic ' + credentials}
        )
        pokemon = Pokemon.query.filter(Pokemon.pokename == 'pokemon1').first()
        self.assertNotEqual(pokemon, None)

    def test_pokemon_choose(self):
        self.client.post(
            '/user/add',
            json={'username': 'user1', 'password': '1234'},
        )
        credentials = base64.b64encode(b'user1:1234').decode('utf-8')

        self.client.post(
            '/pokemon/add',
            json={'pokename': 'pokemon1'},
            headers={'Authorization': 'Basic ' + credentials}
        )
        self.client.post(
            '/pokemon/add',
            json={'pokename': 'pokemon2'},
            headers={'Authorization': 'Basic ' + credentials}
        )

        self.client.post(
            '/pokemon/choose',
            json=['pokemon2'],
            headers={'Authorization': 'Basic ' + credentials}
        )

        user = User.query.filter(User.username == 'user1').first()

        self.assertEqual(len(user.pokemons), 1)
        self.assertEqual(user.pokemons[0].pokename, 'pokemon2')
