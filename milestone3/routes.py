from flask import (
    flash, render_template,
    redirect, request, session, url_for)
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from milestone3 import app, db, mongo
from milestone3.models import Treatment, User


@app.route("/")
@app.route("/get_treatments")
def get_treatments():
    treatments = list(mongo.db.treatments.find())
    return render_template(
        "treatments.html", treatments=treatments)


@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    treatments = list(
        mongo.db.treatments.find({"$text": {"$search": query}}))
    return render_template("treatments.html", treatments=treatments)


@app.route("/add_treatment", methods=["GET", "POST"])
def add_treatment():
    if "user" not in session:
        flash("You need to be logged in to add a treatment")
        return redirect(url_for("get_treatments"))
    if request.method == "POST":
        follow_up = "on" if request.form.get("follow_up") else "off"
        treatment = {
            "treatment_id": request.form.get("treatment_id"),
            "treatment_client": request.form.get("treatment_client"),
            "tusername": request.form.get("tusername"),
            "treatment_name": request.form.get("treatment_name"),
            "treatment_subjective": request.form.get("treatment_subjective"),
            "treatment_observation": request.form.get("treatment_observation"),
            "treatment_rom": request.form.get("treatment_rom"),
            "treatment_special_tests": request.form.get(
                "treatment_special_tests"),
            "treatment_palpation": request.form.get("treatment_palpation"),
            "follow_up": follow_up,
            "treatment_date": request.form.get("treatment_date"),
            "created_by": session["user"]}
        mongo.db.treatments.insert_one(treatment)
        flash("Treatment Successfully Added")
        return redirect(url_for("get_treatments"))
    users = mongo.db.users.find().sort("username", 1)
    # users = list(User.query.order_by(User.fullname).all())
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
            "treatment_client": request.form.get("treatment_client"),
            "treatment_name": request.form.get("treatment_name"),
            "treatment_subjective": request.form.get("treatment_subjective"),
            "treatment_observation": request.form.get("treatment_observation"),
            "treatment_rom": request.form.get("treatment_rom"),
            "treatment_special_tests": request.form.get(
                "treatment_special_tests"),
            "treatment_palpation": request.form.get("treatment_palpation"),
            "follow_up": follow_up,
            "treatment_date": request.form.get("treatment_date"),
            "created_by": session["user"]}
        mongo.db.treatments.replace_one(
            {"_id": ObjectId(treatment_id)}, submit)
        return redirect(url_for("get_treatments"))
        flash("Treatment Successfully Updated")
    users = mongo.db.users.find().sort("fullname", 1)
    # users = list(User.query.order_by(User.fullname).all())
    return render_template(
        "edit_treatment.html", treatment=treatment, users=users)


@app.route("/delete_treatment/<treatment_id>")
def delete_treatment(treatment_id):
    treatment = mongo.db.treatments.find_one({"_id": ObjectId(treatment_id)})
    if "user" not in session or session["user"] != treatment["created_by"]:
        flash("You can only delete your own treatments!")
        return redirect(url_for("get_treatments"))
    mongo.db.treatments.delete_one({"_id": ObjectId(treatment_id)})
    flash("Treatment Successfully Deleted")
    return redirect(url_for("get_treatments"))


@app.route("/get_clients")
def get_clients():
    if "user" not in session or session["user"] != "gadmin":
        flash("You must be admin to manage clients!")
        return redirect(url_for("get_treatments"))

    users = mongo.db.users.find().sort("fullname", 1)
    # user = mongo.db.users.find_one()

    return render_template("clients.html", users=users)


@app.route("/add_client", methods=["GET", "POST"])
def add_client():
    if "user" not in session or session["user"] != "gadmin":
        flash("You must be admin to manage clients!")
        return redirect(url_for("get_treatments"))
    if request.method == "POST":
        user = {
            "username": request.form.get("username"),
            "password": generate_password_hash(request.form.get("password")),
            "fullname": request.form.get("fullname"),
            "dob": request.form.get("dob"),
            "email": request.form.get("email"),
            "phone": request.form.get("phone")
        }
        mongo.db.users.insert_one(user)
        # put the new user into 'session' cookie
        return redirect(url_for("get_clients"))
    return render_template("add_client.html")


@app.route("/edit_client/<user_id>", methods=["GET", "POST"])
def edit_client(user_id):
    treatments = list(mongo.db.treatments.find())
    if "user" not in session or session["user"] != "gadmin":
        flash("You must be admin to manage clients!")
        return redirect(url_for("get_treatments"))
    if request.method == "POST":
        submit = {
            "username": request.form.get("username"),
            "fullname": request.form.get("fullname"),
            "dob": request.form.get("dob"),
            "email": request.form.get("email"),
            "phone": request.form.get("phone")}
        mongo.db.users.replace_one(
            {"_id": ObjectId(user_id)}, submit)
        flash("Successfully Updated")
        return redirect(url_for("get_clients"))
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    return render_template(
        "edit_client.html", treatments=treatments, user=user)


@app.route("/delete_client/<user_id>")
def delete_client(user_id):
    if session["user"] != "gadmin":
        flash("You must be admin to manage clients!")
        return redirect(url_for("get_treatments"))
    mongo.db.users.delete_one({"_id": ObjectId(user_id)})
    flash("Client Successfully Deleted")
    # user = User.query.get_or_404(user_id)
    # db.session.delete(user)
    # db.session.commit()
    # mongo.db.treatments.delete_many({"user_id": str(user_id)})
    return redirect(url_for("get_clients"))


@app.route("/report")
def report():
    # users = list(User.query.all())
    users = list(mongo.db.users.find())
    treatments = list(mongo.db.treatments.find())
    return render_template("report.html", treatments=treatments, users=users)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username")})
            # User.user_name == request.form.get("username").lower()).all()
        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username"),
            "password": generate_password_hash(request.form.get("password")),
            "fullname": request.form.get("fullname"),
            "dob": request.form.get("dob"),
            "email": request.form.get("email"),
            "phone": request.form.get("phone")
        }
        mongo.db.users.insert_one(register)

        # user = User(
        #     user_name=request.form.get("username").lower(),
        #     password=generate_password_hash(request.form.get("password")),
        #     fullname=request.form.get("fullname"),
        #     dob=request.form.get("dob"),
        #     email=request.form.get("email"),
        #     phone=request.form.get("phone"))
        # db.session.add(user)
        # db.session.commit()
        # # put the new user into 'session' cookie
        session["user"] = request.form.get("username")
        flash("Registration Successful!")
        return redirect(url_for(
            "profile", username=session["user"]))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})
        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                        session["user"] = request.form.get("username").lower()
                        flash("Welcome {} logged in.".format(
                            request.form.get("username")))
                        return redirect(url_for('get_treatments'))
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
    username = mongo.db.users.find_one(
        {"username": session["user"]})
    if session["user"]:
        return render_template("profile.html", username=username)
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))
