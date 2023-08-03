import os

from flask import current_app as app
from flask import request, session, jsonify
from flask_cors import cross_origin
from flask_security import (
    hash_password,
    verify_password,
    auth_token_required,
    roles_accepted,
)

from .database import db
from .models import *

with app.app_context():
    # dbpath = os.path.abspath(
    #     os.path.join(os.path.dirname(__file__), "./../instance/testdb.sqlite3")
    # )
    # if os.path.exists(dbpath):
    #     os.remove(dbpath)
    db.create_all()
    # app.security.datastore.find_or_create_role(name="admin", description="root admin")
    # app.security.datastore.find_or_create_role(
    #     name="manager", description="theatre manager"
    # )
    # app.security.datastore.find_or_create_role(
    #     name="customer", description="normal user"
    # )
    # db.session.commit()
    # app.security.datastore.create_user(
    #     email="admin@cookmyshow.com",
    #     password=hash_password("mypassword"),
    #     roles=["admin"],
    #     username="cookmyshow_admin",
    # )
    # db.session.commit()


@app.route("/", methods=["GET"])
def home():
    return jsonify({"resp": "ok", "msg": "Welcome to CookMyShow Application"})


@app.route("/register_page", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = request.get_json()
        username, email, pwd, role_name = (
            data["username"],
            data["email"],
            data["password"],
            data["role"],
        )

        if app.security.datastore.find_user(username=username):
            return jsonify({"resp": "not ok", "msg": "Username already taken."})
        elif app.security.datastore.find_user(email=email):
            return jsonify({"resp": "not ok", "msg": "Email already registered."})
        else:
            app.security.datastore.create_user(
                email=email,
                password=hash_password(pwd),
                roles=[role_name],
                username=username,
            )
            db.session.commit()
            return jsonify({"resp": "ok", "msg": "Account created."})
    else:
        return jsonify({"resp": "ok", "msg": "Getting signup page"})


@app.route("/login_page", methods=["GET", "POST"])
@auth_token_required
def login():
    if request.method == "POST":
        data = request.get_json()
        email, pwd, role = data["email"], data["password"], data["role"]

        user = app.security.datastore.find_user(email=email)

        if not user:
            return jsonify({"resp": "not ok", "msg": "Invalid credentials"})

        if verify_password(pwd, user.password):
            user_data = {"email": email, "username": user.username, "role": role}
            for k, v in user_data.items():
                session[k] = v
            return jsonify(
                {"resp": "ok", "msg": "Login successful", "stuff": user_data}
            )
        else:
            app.logger.debug(f"{pwd}, {user.password}")
            return jsonify({"resp": "not ok", "msg": "Incorrect password"})

    else:
        return jsonify({"resp": "ok", "msg": "Getting login page"})


@app.route("/logout_page", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"resp": "ok", "msg": "Logged out successfully"})


@app.route("/admin/dashboard", methods=["GET"])
@auth_token_required
@roles_accepted("admin")
def admin_dashboard():
    theatre_query = Theatre.query.all()
    theatres = [
        {
            "id": theatre.id,
            "name": theatre.name,
            "capacity": theatre.capacity,
            "address": theatre.address,
            "manager": {
                "id": theatre.manager,
                "username": app.security.datastore.find_user(
                    id=theatre.manager
                ).username,
            }
            if theatre.manager
            else theatre.manager,
            "shows": [
                {"id": show.id, "title": show.title, "time": show.time}
                for show in theatre.shows
            ],
        }
        for theatre in theatre_query
    ]

    # theatreShows = {theatre.id:{"id":show.id, "title":show.title, "time":show.time for show in theatre.shows} for theatre in theatres}
    # theatreShows = {}
    # for theatre in theatres:
    #     for show in theatre.shows:
    #         theatreShows[theatre.id] = {
    #             "id": show.id,
    #             "title": show.title,
    #             "time": show.time,
    #         }

    # theatreShowIds = {
    #     theatre.id: TheatreShows.query.with_entities(TheatreShows.show_id)
    #     .filter(TheatreShows.theatre_id == theatre.id)
    #     .all()
    #     for theatre in theatre_query
    # }

    # theatreShows = {}
    # for theatreId, showIdsList in theatreShowIds.items():
    #     theatreShows[theatreId] = [
    #         {
    #             "id": (sh := Show.query.filter_by(id=show_id_tup[0]).first()).id,
    #             "title": sh.title,
    #             "time": sh.duration,
    #         }
    #         for show_id_tup in showIdsList
    #     ]

    return jsonify(
        {"resp": "ok", "msg": "Theatre and show list extracted.", "stuff": theatres}
    )


@app.route("/theatre/add_new", methods=["GET", "POST"])
@auth_token_required
@roles_accepted("admin")
def add_new_theatre():
    # add manager in post request
    if request.method == "POST":
        data = request.get_json()
        name, address, capacity, manager = (
            data["name"],
            data["address"],
            data["capacity"],
            data["manager"],
        )
        th = Theatre(name=name, address=address, capacity=capacity, manager=manager)
        db.session.add(th)
        db.session.commit()
        return jsonify({"resp": "ok", "msg": "new theatre added."})
    else:
        mgrIds = (
            UserRoles.query.with_entities(UserRoles.user_id)
            .filter(UserRoles.role_name == "manager")
            .all()
        )
        managers = [
            {
                "id": (mgr := app.security.datastore.find_user(id=mgr_id_tup[0])).id,
                "username": mgr.username,
            }
            for mgr_id_tup in mgrIds
        ]
        return jsonify({"resp": "ok", "msg": "Page loaded.", "stuff": managers})


@app.route("/theatre/<int:theatre_id>", methods=["GET", "POST", "DELETE"])
@auth_token_required
def get_update_delete_theatre(theatre_id):
    theatre = Theatre.query.filter_by(id=theatre_id).first()
    if request.method == "POST":
        data = request.get_json()
        name, address, capacity, manager = (
            data["name"],
            data["address"],
            data["capacity"],
            data["manager"],
        )
        theatre.name, theatre.address, theatre.capacity, theatre.manager = (
            name,
            address,
            capacity,
            manager,
        )
        db.session.add(theatre)
        db.session.commit()
        return jsonify({"resp": "ok", "msg": "theatre details updated."})
    elif request.method == "GET":
        # showIds = (
        #     TheatreShows.query.with_entities(TheatreShows.show_id)
        #     .filter(TheatreShows.theatre_id == theatre_id)
        #     .all()
        # )

        # shows = [
        #     {
        #         "id": (sh := Show.query.filter_by(id=show_id_tup[0]).first()).id,
        #         "name": sh.title,
        #         "time": sh.duration,
        #     }
        #     for show_id_tup in showIds
        # ]
        mgrIds = (
            UserRoles.query.with_entities(UserRoles.user_id)
            .filter(UserRoles.role_name == "manager")
            .all()
        )
        manager_list = [
            {
                "id": (mgr := app.security.datastore.find_user(id=mgr_id_tup[0])).id,
                "username": mgr.username,
            }
            for mgr_id_tup in mgrIds
        ]
        theatre_data = {
            "id": theatre.id,
            "name": theatre.name,
            "address": theatre.address,
            "capacity": theatre.capacity,
            "manager": theatre.manager,
            "shows": [
                {"id": show.id, "title": show.title, "time": show.time}
                for show in theatre.shows
            ],
        }
        return jsonify(
            {
                "resp": "ok",
                "msg": "theatre data extracted.",
                "stuff": {"theatre_data": theatre_data, "manager_list": manager_list},
            }
        )
    else:
        db.session.delete(theatre)
        db.session.commit()
        return jsonify({"resp": "ok", "msg": "theatre removed."})


@app.route("/manager/<string:username>/dashboard", methods=["GET"])
@auth_token_required
@roles_accepted("manager")
def manager_dashboard(username):
    user = app.security.datastore.find_user(username=username)
    mgr_id = user.id
    # app.logger.debug(mgr_id)

    theatre_query = Theatre.query.filter_by(manager=mgr_id).all()
    theatres = [
        {
            "id": theatre.id,
            "name": theatre.name,
            "address": theatre.address,
            "capacity": theatre.capacity,
            "shows": [
                {"id": show.id, "title": show.title, "time": show.time}
                for show in theatre.shows
            ],
        }
        for theatre in theatre_query
    ]
    app.logger.debug(theatres)
    # app.logger.debug(theatres)

    # theatreShowIds = {
    #     theatre.id: TheatreShows.query.with_entities(TheatreShows.show_id)
    #     .filter(TheatreShows.theatre_id == theatre.id)
    #     .all()
    #     for theatre in theatre_query
    # }

    # theatreShows = {}
    # for theatreId, showIdsList in theatreShowIds.items():
    #     theatreShows[theatreId] = [
    #         {
    #             "id": (sh := Show.query.filter_by(id=show_id_tup[0]).first()).id,
    #             "name": sh.title,
    #             "time": sh.duration,
    #         }
    #         for show_id_tup in showIdsList
    #     ]
    # theatreShows = {}
    # for theatre in theatres:
    #     for show in theatre.shows:
    #         theatreShows[theatre.id] = {
    #             "id": show.id,
    #             "title": show.title,
    #             "time": show.time,
    #         }

    return jsonify(
        {"resp": "ok", "msg": "Theatre and show list extracted.", "stuff": theatres}
    )


@app.route("/manager/<string:username>/show/add_new", methods=["GET", "POST"])
@auth_token_required
@roles_accepted("manager")
def add_new_show(username):
    if request.method == "POST":
        user = app.security.datastore.find_user(username=username)
        mgr_id = user.id
        data = request.get_json()
        title, duration, tags, theatres = (
            data["title"],
            data["duration"],
            data["tags"],
            data["theatres"],
        )
        for theatre in theatres:
            sh = Show(
                title=title,
                duration=duration,
                tags=tags,
                price=theatre["price"],
                time=datetime.strptime(theatre["time"], "%Y-%m-%dT%H:%M:%S.%f%z"),
                seats=theatre["seats"],
            )
            db.session.add(sh)
            db.session.commit()
            th_sh = TheatreShows(theatre_id=theatre["id"], show_id=sh.id)
            db.session.add(th_sh)
        db.session.commit()
        return jsonify({"resp": "ok", "msg": "new show added."})
    else:
        user = app.security.datastore.find_user(username=username)
        mgr_id = user.id

        theatre_query = Theatre.query.filter_by(manager=mgr_id).all()
        theatres = [
            {
                "id": theatre.id,
                "name": theatre.name,
                "capacity": theatre.capacity,
                "address": theatre.address,
                "selected": False,
                "price": "",
                "time": "",
                "seats": "",
            }
            for theatre in theatre_query
        ]

        return jsonify(
            {
                "resp": "ok",
                "msg": "Add Shows page loaded.",
                "stuff": theatres,
            }
        )


@app.route("/<string:username>/show/<int:show_id>", methods=["GET", "POST", "DELETE"])
@auth_token_required
def get_update_delete_show(username, show_id):
    show = Show.query.filter_by(id=show_id).first()
    if request.method == "POST":
        data = request.get_json()
        title, duration, tags, price, time, seats, updated_theatre_ids = (
            data["title"],
            data["duration"],
            data["tags"],
            data["price"],
            datetime.strptime(data["time"], "%Y-%m-%dT%H:%M"),
            data["seats"],
            data["theatres"],
        )

        theatre_ids = [theatre.id for theatre in show.hosting_theatres]

        # theatre_ids = [
        #     theatre_id_tup[0]
        #     for theatre_id_tup in TheatreShows.query.with_entities(
        #         TheatreShows.theatre_id
        #     )
        #     .filter(TheatreShows.show_id == show_id)
        #     .all()
        # ]
        for theatre_id in theatre_ids:
            if theatre_id not in updated_theatre_ids:
                th_sh = TheatreShows.query.filter_by(
                    theatre_id=theatre_id, show_id=show_id
                )
                db.session.delete(th_sh)

        for theatre_id in updated_theatre_ids:
            if theatre_id not in theatre_ids:
                th_sh = TheatreShows(theatre_id=theatre_id, show_id=show_id)
                db.session.add(th_sh)

        show.title, show.duration, show.tags, show.price, show.time, show.seats = (
            title,
            duration,
            tags,
            price,
            time,
            seats,
        )
        db.session.add(show)
        db.session.commit()
        return jsonify({"resp": "ok", "msg": "show details updated."})
    elif request.method == "GET":
        user = app.security.datastore.find_user(username=username)
        mgr_id = user.id

        theatre_query = Theatre.query.filter_by(manager=mgr_id).all()

        theatres = [
            {
                "id": theatre.id,
                "name": theatre.name,
                "address": theatre.address,
                "capacity": theatre.capacity,
                "manager": theatre.manager,
            }
            for theatre in show.hosting_theatres
        ]
        managed_theatres = [
            {
                "id": theatre.id,
                "name": theatre.name,
                "capacity": theatre.capacity,
                "address": theatre.address,
                "selected": (theatre.id == theatres[0]["id"]),
                "price": "",
                "time": "",
                "seats": "",
            }
            for theatre in theatre_query
        ]
        show_data = {
            "id": show.id,
            "title": show.title,
            "duration": show.duration,
            "tags": show.tags,
            "price": show.price,
            "time": show.time,
            "seats": show.seats,
            "ratings": show.rating,
            "theatres": theatres[0],
        }

        data = {"show_data": show_data, "theatre_list": managed_theatres}
        return jsonify({"resp": "ok", "msg": "show data extracted.", "stuff": data})
    else:
        show.hosting_theatres = []
        db.session.delete(show)
        db.session.commit()
        return jsonify({"resp": "ok", "msg": "show removed."})
