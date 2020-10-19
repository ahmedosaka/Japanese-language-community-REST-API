from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from config import Config
from sqlalchemy.orm import sessionmaker

Config = Config()

db = SQLAlchemy()

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI,echo=True)
Session = sessionmaker(bind=engine)
