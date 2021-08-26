from pokeapi.app import app, db
from sqlalchemy.exc import OperationalError
from time import sleep


if __name__ == '__main__':

    while True:
        try:
            db.create_all()
            break
        except OperationalError:
            print("Oops! Database is not available. Try again...")
            sleep(5)
    app.run(port=5000, host='0.0.0.0')
