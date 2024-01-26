from flask import Flask
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# routes imports
from app.routes.main import main