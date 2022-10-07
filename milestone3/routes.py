from flask import (
    flash, render_template,
    redirect, request, session, url_for)
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from milestone3 import app, db, mongo
from milestone3.models import Users, Client, Treatment, Therapist


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
        is_urgent = "on" if request.form.get("is_urgent") else "off"
        treatment = {
            "client_id": request.form.get("client_id"),
            "treatment_name": request.form.get("treatment_name"),
            "treatment_description": request.form.get("treatment_description"),
            "is_urgent": is_urgent,
            "due_date": request.form.get("due_date"),
            "created_by": session["user"]}
        mongo.db.treatments.insert_one(treatment)
        flash("Treatment Successfully Added")
        return redirect(url_for("get_treatments"))

    clients = list(Client.query.order_by(Client.client_name).all())
    return render_template("add_treatment.html", clients=clients)


@app.route("/edit_treatment/<treatment_id>", methods=["GET", "POST"])
def edit_treatment(treatment_id):
    treatment = mongo.db.treatments.find_one({"_id": ObjectId(treatment_id)})
    if "user" not in session or session["user"] != treatment["created_by"]:
        flash("You can only edit your own treatments!")
        return redirect(url_for("get_treatments"))
        
    if request.method == "POST":
        is_urgent = "on" if request.form.get("is_urgent") else "off"
        submit = {
            "client_id": request.form.get("client_id"),
            "treatment_name": request.form.get("treatment_name"),
            "treatment_description": request.form.get("treatment_description"),
            "is_urgent": is_urgent,
            "due_date": request.form.get("due_date"),
            "created_by": session["user"]}
        mongo.db.treatments.update({"_id": ObjectId(treatment_id)}, submit)
        flash("Treatment Successfully Updated")

    clients = list(Client.query.order_by(Client.client_name).all())
    return render_template("edit_treatment.html", treatment=treatment, clients=clients)


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

    clients = list(Client.query.order_by(Client.client_name).all())
    return render_template("clients.html", clients=clients)


@app.route("/add_client", methods=["GET", "POST"])
def add_client():
    if "user" not in session or session["user"] != "gadmin":
        flash("You must be admin to manage clients!")
        return redirect(url_for("get_treatments"))

    if request.method == "POST":
        client = Client(client_name=request.form.get("client_name"))
        db.session.add(client)
        db.session.commit()
        return redirect(url_for("get_clients"))
    return render_template("add_client.html")


@app.route("/edit_client/<int:client_id>", methods=["GET", "POST"])
def edit_client(client_id):
    if "user" not in session or session["user"] != "gadmin":
        flash("You must be admin to manage clients!")
        return redirect(url_for("get_treatments"))
    
    client = Client.query.get_or_404(client_id)
    if request.method == "POST":
        client.client_name = request.form.get("client_name")
        db.session.commit()
        return redirect(url_for("get_clients"))
    return render_template("edit_client.html", client=client)


@app.route("/delete_client/<int:client_id>")
def delete_client(client_id):
    if session["user"] != "gadmin":
        flash("You must be admin to manage clients!")
        return redirect(url_for("get_treatments"))

    client = Client.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    mongo.db.treatments.delete_many({"client_id": str(client_id)})
    return redirect(url_for("get_clients"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = Users.query.filter(Users.user_name == \
            request.form.get("username").lower()).all()
        
        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))
        
        user = Users(
            user_name=request.form.get("username").lower(),
            password=generate_password_hash(request.form.get("password"))
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
        existing_user = Users.query.filter(Users.user_name == \
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