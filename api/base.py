from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_jwt_extended import JWTManager


db = SQLAlchemy()
jwt = JWTManager()