from flask_security import UserMixin, RoleMixin
from datetime import datetime
from .database import db


# Defines the user model which can be used by admin, manager or customer
class User(db.Model, UserMixin):
    """
    User model
    """

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), unique=True, nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
    active = db.Column(db.Boolean)
    roles = db.relationship(
        "Role", secondary="user_roles", backref=db.backref("role_users", lazy=True)
    )
    shows = db.relationship(
        "Show", secondary="booked_shows", backref=db.backref("customers", lazy=True)
    )


class Theatre(db.Model):
    """
    Theatre model
    """

    __tablename__ = "theatres"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    manager = db.Column(db.String, nullable=True)
    shows = db.relationship(
        "Show",
        secondary="hosted_shows",
        backref=db.backref("hosting_theatres", lazy=True),
        cascade="all, delete",
    )


class Show(db.Model):
    """
    Show model
    """

    __tablename__ = "shows"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    tags = db.Column(db.String(400), nullable=True)
    price = db.Column(db.Float, nullable=False)
    time = db.Column(db.DateTime(timezone="Asia/Kolkata"), nullable=False)
    seats = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, default=0)


class Role(db.Model, RoleMixin):
    """
    Role model
    """

    __tablename__ = "roles"
    name = db.Column(db.String(100), unique=True, primary_key=True)
    description = db.Column(db.String(200))
    # permissions = db.Column(db.String(200), nullable=True)


class UserRoles(db.Model):
    """
    User <-> Role relationship
    """

    __tablename__ = "user_roles"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column("user_id", db.Integer, db.ForeignKey("users.id"))
    role_name = db.Column("role_name", db.Integer, db.ForeignKey("roles.name"))


class UserShows(db.Model):
    """
    Customer <-> Show relationship
    """

    __tablename__ = "booked_shows"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column("user_id", db.Integer, db.ForeignKey("users.id"))
    show_id = db.Column("show_id", db.Integer, db.ForeignKey("shows.id"))


class TheatreShows(db.Model):
    """
    Theatre <-> show relationship
    """

    __tablename__ = "hosted_shows"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    theatre_id = db.Column("theatre_id", db.Integer, db.ForeignKey("theatres.id"))
    show_id = db.Column("show_id", db.Integer, db.ForeignKey("shows.id"))


class UserHistory(db.Model):
    __tablename__ = "watched_shows"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column("user_id", db.Integer, db.ForeignKey("users.id"))
    show_id = db.Column("show_id", db.Integer, db.ForeignKey("shows.id"))
    rating = db.Column(db.Integer, default=0)
