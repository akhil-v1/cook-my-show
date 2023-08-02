import os

from flask import current_app as app
from flask import request, session, jsonify
from flask_cors import cross_origin
from flask_security import hash_password, verify_password, current_user, auth_token_required

from .database import db
from .models import *

with app.app_context():
    # dbpath = os.path.abspath(os.path.join(os.path.dirname(__file__), "./../instance/testdb.sqlite3"))
    # if os.path.exists(dbpath):
    #     os.remove(dbpath)
    db.create_all()
    # app.security.datastore.find_or_create_role(name="admin", description="root admin")
    # app.security.datastore.find_or_create_role(name="manager", description="theatre manager")
    # app.security.datastore.find_or_create_role(name="customer", description="normal user")
    # db.session.commit()
    # app.security.datastore.create_user(email="admin@cookmyshow.com", password=hash_password("mypassword"), roles=["admin"], username="cookmyshow_admin")
    # db.session.commit()

@app.route("/", methods=["GET"])
def home():
    app.logger.debug("Home")
    return jsonify({"resp":"ok", "msg":"Welcome to CookMyShow Application"})

@app.route("/register_page", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = request.get_json()
        username, email, pwd, role_name = data["username"], data["email"], data["password"], data["role"]

        if app.security.datastore.find_user(username=username):
            return jsonify({"resp":"not ok", "msg":"Username already taken."})
        elif app.security.datastore.find_user(email=email):
            return jsonify({"resp":"not ok", "msg":"Email already registered."})
        else:
            app.security.datastore.create_user(email=email, password=hash_password(pwd), 
                                               roles=[role_name], username=username)
            db.session.commit()
            return jsonify({"resp":"ok", "msg":"Account created."})
    else:
        return jsonify({"resp":"ok", "msg":"Getting signup page"})


@app.route("/login_page", methods=["GET", "POST"])
@auth_token_required
def login():
    # add a role check
    if request.method == "POST":
        data = request.get_json()
        email, pwd, role = data["email"], data["password"], data["role"]

        user = app.security.datastore.find_user(email=email)
        
        if not user:
            return jsonify({"resp":"not ok", "msg": "Invalid credentials"})
        
        if verify_password(pwd, user.password):
            user_data = {"email": email,
                         "username": user.username,
                         "role": role}  
            for k, v in user_data.items():
                session[k] = v
            return jsonify({"resp":"ok", "msg":"Login successful", "stuff":user_data})
        else:
            app.logger.debug(f"{pwd}, {user.password}")
            return jsonify({"resp": "not ok", "msg": "Incorrect password"})

    else:
        return jsonify({"resp":"ok", "msg":"Getting login page"})

@app.route("/logout_page", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"resp":"ok", "msg":"Logged out successfully"})

@app.route("/admin/dashboard", methods=["GET", "POST"])
@auth_token_required
def admin_dashboard():
    if request.method == "POST":
        pass
    else:
        # send managed, unamanged theatres
        # add a role requirement for only admin access
        # add a manager to theatre and send it to display with other details
        theatre_query = Theatre.query.all()
        theatres = [{"id": theatre.id, "name": theatre.name, "capacity":theatre.capacity, "address":theatre.address} for theatre in theatre_query]
        # app.logger.debug(theatres)
        # for theatre in theatres:
        #     app.logger.debug(f"{theatre.id}, {theatre.name}")
        theatreShowIds = {theatre.id: TheatreShows.query.with_entities(TheatreShows.show_id)
                        .filter(TheatreShows.theatre_id==theatre.id).all()   
                        for theatre in theatre_query}
        # app.logger.debug(theatreShowIds)
        theatreShows = {}

        for theatreId, showIdsList in theatreShowIds.items():
            theatreShows[theatreId] = [{"id":(sh:=Show.query.filter_by(id=show_id_tup[0]).first()).id,
                                        "name": sh.title, "time":sh.duration}
                                    for show_id_tup in showIdsList]
        
        data = {"theatres":theatres,
                "theatreShows": theatreShows}
        app.logger.debug(data)
        # app.logger.debug("Unauthorized")
        return jsonify({"resp": "ok", "msg": "Theatre and show list extracted.", "stuff":data})


@app.route("/theatre/<int:theatre_id>", methods=["GET", "POST"])
@auth_token_required
def theatre_page(theatre_id):
    if request.method=="POST":
        pass
    else:
        if (theatre_id == 0):
            return jsonify({"resp":"ok", "msg":"Theatre page loaded successfully."})
        else:
            theatre = Theatre.query.filter_by(id=theatre_id)
            showIds = TheatreShows.query.with_entities(TheatreShows.show_id)\
                    .filter(TheatreShows.theatre_id==theatre_id).all()
            
            shows = [{"id":(sh:=Show.query.filter_by(id=show_id_tup[0])).first().id,
                      "name":sh.title,
                      "time":sh.duration} 
                      for show_id_tup in showIds]
            theatre_data = {"name": theatre.name,
                            "place": theatre.address,
                            "capacity": theatre.capacity,
                            "shows":shows}
            return jsonify({"resp":"ok", "msg":"theatre data extracted.", "stuff":theatre_data})

@app.route("/theatre/<int:theatre_id>/update", methods=["GET", "POST"])
@auth_token_required
def update_theatre():
    pass

@app.route("/theatre/<int:theatre_id>/remove", methods=["GET", "POST"])
@auth_token_required
def delete_theatre():
    pass


@app.route("/manager/<int:mgr_id>/dashboard", methods=["GET", "POST"])
@auth_token_required
def manager_dashboard(mgr_id):
    # send theatres managed by mgr_id
    # add role requirement for only manager access
    app.logger.debug("Unauthorized")
    return jsonify({"resp": "ok", "msg": "Hello"})

@app.route("/theatre/<int:theatre_id>/home", methods=["GET"])
@auth_token_required
def show_theatre():
    pass