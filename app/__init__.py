from dotenv import load_dotenv
from flask import Flask
from flask_pymongo import PyMongo

load_dotenv()

app = Flask(__name__)
app.config.from_envvar('MONGO_URL')

mongo = PyMongo(app)

# routes imports
from app.routes.main import main
from app.routes.part import part
from app.routes.category import category