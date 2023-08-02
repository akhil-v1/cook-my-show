from flask_security import SQLAlchemySessionUserDatastore, SQLAlchemyUserDatastore
from .database import db
from .models import User, Role

user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)