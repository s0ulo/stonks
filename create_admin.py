from getpass import getpass
import sys

from stonks_app import create_app
from stonks_app.db import db
from stonks_app.user.models import User

app = create_app()

with app.app_context():
    username = input("Set admin username: ")

    if User.query.filter(User.username == username).count():
        print(f"User `{username}` already exists.\n")
        sys.exit(0)

    password1 = getpass("Set admin password: ")
    password2 = getpass("Verify admin password: ")

    if not password1 == password2:
        print("Error! Passwords don't match!")
        sys.exit(0)

    new_user = User(username=username, role="admin")
    new_user.set_password(password1)

    db.session.add(new_user)
    db.session.commit()
    print(f"New user registered with id={new_user.id}")
