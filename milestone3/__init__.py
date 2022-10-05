import os
import re
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
if os.path.exists("env.py"):
    import env  # noqa


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

if os.environ.get("DEVELOPMENT") == "True":
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DB_URL") 
else:
    uri = os.environ.get("DATABASE_URL")
    if uri.startswith("postgres://"):
        uri = ("postgres://omeczhtjfbhlku:614b0d8eeca9037347b3ad4a26f43053e4a4fba0995deb76ae09e1a740d954f4@ec2-34-247-72-29.eu-west-1.compute.amazonaws.com:5432/d52are1giln6ji")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL") 

db = SQLAlchemy(app)

from milestone3 import routes  # noqa