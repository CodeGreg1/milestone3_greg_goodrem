from flask import (
    flash, render_template,
    redirect, request, session, url_for)
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from milestone3 import app, db, mongo
from milestone3.models import User, Client, Treatment
# , Therapist


@app.route("/")
@app.route("/get_treatments")
def get_treatments():
    treatments = list(mongo.db.treatments.find())
    return render_template("treatments.html", treatments=treatments)


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    treatments = list(mongo.db.treatments.find({"$text": {"$search": query}}))
    return render_template("treatments.html", treatments=treatments)


@app.route("/add_treatment", methods=["GET", "POST"])
def add_treatment():
    if "user" not in session:
        flash("You need to be logged in to add a treatment")
        return redirect(url_for("get_treatments"))
        
    if request.method == "POST":
        follow_up = "on" if request.form.get("follow_up") else "off"
        #"user_id": request.form.get("user_id"),
        treatment = {
            "treatment_name": request.form.get("treatment_name"),
            "treatment_subjective": request.form.get("treatment_subjective"),
            "treatment_observation": request.form.get("treatment_observation"),
            "treatment_rom": request.form.get("treatment_rom"),
            "treatment_special_tests": request.form.get("treatment_special_tests"),
            "treatment_palpation": request.form.get("treatment_palpation"),
            "follow_up": follow_up,
            "treatment_date": request.form.get("treatment_date"),
            "created_by": session["user"]}
        mongo.db.treatments.insert_one(treatment)
        user = User(
            fullname=request.form.get("fullname"))
        
        flash("Treatment Successfully Added")
        return redirect(url_for("get_treatments"))

    users = list(User.query.order_by(User.fullname).all())
    return render_template("add_treatment.html", users=users)


@app.route("/edit_treatment/<treatment_id>", methods=["GET", "POST"])
def edit_treatment(treatment_id):
    treatment = mongo.db.treatments.find_one({"_id": ObjectId(treatment_id)})
    if "user" not in session or session["user"] != treatment["created_by"]:
        flash("You can only edit your own treatments!")
        return redirect(url_for("get_treatments"))
        
    if request.method == "POST":
        follow_up = "on" if request.form.get("follow_up") else "off"
        submit = {
            "user_id": request.form.get("user_id"),
            "treatment_name": request.form.get("treatment_name"),
            "treatment_description": request.form.get("treatment_description"),
            "follow_up": follow_up,
            "treatment_date": request.form.get("treatment_date"),
            "created_by": session["user"]}
        mongo.db.treatments.update({"_id": ObjectId(treatment_id)}, submit)
        flash("Treatment Successfully Updated")

    users = list(User.query.order_by(User.fullname).all())
    return render_template("edit_treatment.html", treatment=treatment, users=users)


@app.route("/delete_treatment/<treatment_id>")
def delete_treatment(treatment_id):
    treatment = mongo.db.treatments.find_one({"_id": ObjectId(treatment_id)})

    if "user" not in session or session["user"] != treatment["created_by"]:
        flash("You can only delete your own treatments!")
        return redirect(url_for("get_treatments"))
    
    mongo.db.treatments.remove({"_id": ObjectId(treatment_id)})
    flash("Treatment Successfully Deleted")
    return redirect(url_for("get_treatments"))


@app.route("/get_clients")
def get_clients():
    if "user" not in session or session["user"] != "gadmin":
        flash("You must be admin to manage clients!")
        return redirect(url_for("get_treatments"))

    users = list(User.query.order_by(User.fullname).all())
    return render_template("clients.html", users=users)
# @app.route("/get_clients")
# def get_clients():
#     if "user" not in session or session["user"] != "gadmin":
#         flash("You must be admin to manage clients!")
#         return redirect(url_for("get_treatments"))

#     clients = list(Client.query.order_by(Client.client_name).all())
#     return render_template("clients.html", clients=clients)


@app.route("/add_client", methods=["GET", "POST"])
def add_client():
    if "user" not in session or session["user"] != "gadmin":
        flash("You must be admin to manage clients!")
        return redirect(url_for("get_treatments"))

    if request.method == "POST":

        client = Client(
            client_name=request.form.get("client_name"),
            client_dob=request.form.get("client_dob"),
            client_email=request.form.get("client_email"),
            client_phone=request.form.get("client_phone")
        )
        db.session.add(client)
        db.session.commit()
        return redirect(url_for("get_clients"))
    return render_template("add_client.html")


@app.route("/edit_client/<int:user_id>", methods=["GET", "POST"])
def edit_client(user_id):
    if "user" not in session or session["user"] != "gadmin":
        flash("You must be admin to manage clients!")
        return redirect(url_for("get_treatments"))
    
    user = User.query.get_or_404(user_id)
    if request.method == "POST":
        user.fullname = request.form.get("fullname")
        db.session.commit()
        return redirect(url_for("get_clients"))
    return render_template("edit_client.html", user=user)


@app.route("/delete_client/<int:user_id>")
def delete_client(user_id):
    if session["user"] != "gadmin":
        flash("You must be admin to manage clients!")
        return redirect(url_for("get_treatments"))

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    mongo.db.treatments.delete_many({"user_id": str(user_id)})
    return redirect(url_for("get_clients"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = User.query.filter(User.user_name == \
            request.form.get("username").lower()).all()
        
        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))
        
        user = User(
            user_name=request.form.get("username").lower(),
            password=generate_password_hash(request.form.get("password")),
            fullname=request.form.get("fullname"),
            dob=request.form.get("dob"),
            email=request.form.get("email"),
            phone=request.form.get("phone")
        )
        
        db.session.add(user)
        db.session.commit()

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = User.query.filter(User.user_name == \
            request.form.get("username").lower()).all()
            #request.form.get("username").lower()).all()

        if existing_user:
            print(request.form.get("username"))
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user[0].password, request.form.get("password")):
                        session["user"] = request.form.get("username").lower()
                        flash("Welcome, {}".format(
                            request.form.get("username")))
                        return redirect(url_for(
                            "profile", username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
        
    if "user" in session:
        return render_template("profile.html", username=session["user"])

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))