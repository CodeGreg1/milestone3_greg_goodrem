txt
@app.route("/edit_user/<int:user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    if "user" not in session or session["user"] != "admin":
        flash("You must be admin to manage users!")
        return redirect(url_for("get_treatments"))
    
    user = user.query.get_or_404(user_id)
    if request.method == "POST":
        user.user_name = request.form.get("user_name")
        db.session.commit()
        return redirect(url_for("get_users"))
    return render_template("edit_user.html", user=user)


    user.fullname = request.form.get("text(fullname)")
        user.dob = request.form.get("dob")
        user.email = request.form.get("email")
        user.phone = request.form.get("phone")
        user.user_name = request.form.get("username")




@app.route("/edit_client/<int:user_id>", methods=["GET", "POST"])
def edit_client(user_id):
    treatments = list(mongo.db.treatments.find())
    if "user" not in session or session["user"] != "gadmin":
        flash("You must be admin to manage clients!")
        return redirect(url_for("get_treatments"))
    user = User.query.get_or_404(user_id)
    # print("Pre User posted")
    # user = list(User.query.order_by(user_id))
    # user = list(db.session.User.find())
    # print("pre post")
        
    user = User(
        user_name=request.form.get("username"),
        # password=generate_password_hash(request.form.get("password")),
        fullname=request.form.get("fullname"),
        dob=request.form.get("dob"),
        email=request.form.get("email"),
        phone=request.form.get("phone"))
    print("pre commit")
    if request.method == "POST":
        # db.create_scoped_session(db.session.commit())
        # print("User posted")
        # db.app.session.commit()
        db.session.commit()
        print("post commit")
        return redirect(url_for("get_clients"))
    return render_template(
        "edit_client.html", user=user, treatments=treatments)
# @app.route("/update_client/<int:user_id>")
# def update_client(user_id):
#     if session["user"] != "gadmin":
#         flash("You must be admin to manage clients!")
#         return redirect(url_for("get_treatments"))
#     user = User.query.get_or_404(user_id)

#     db.session.update(user)
#     db.session.commit()
#     # mongo.db.treatments.delete_many({"user_id": str(user_id))
#     db.User.update_many("user_id", str(user_id))
#     return "edit_client.html", user=user, treatments=treatments)


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


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
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
    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        return render_template("profile.html", username=username)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # remove user from session cookie
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/add_treatment", methods=["GET", "POST"])
def add_treatment():
    if request.method == "POST":
        is_urgent = "on" if request.form.get("is_urgent") else "off"
        treatment = {
            "user_name": request.form.get("user_name"),
            "treatment_name": request.form.get("treatment_name"),
            "treatment_description": request.form.get("treatment_description"),
            "is_urgent": is_urgent,
            "due_date": request.form.get("due_date"),
            "created_by": session["user"]
        }
        mongo.db.treatments.insert_one(treatment)
        flash("treatment Successfully Added")
        return redirect(url_for("get_treatments"))

    users = mongo.db.users.find().sort("user_name", 1)
    return render_template("add_treatment.html", users=users)


@app.route("/edit_treatment/<treatment_id>", methods=["GET", "POST"])
def edit_treatment(treatment_id):
    if request.method == "POST":
        is_urgent = "on" if request.form.get("is_urgent") else "off"
        submit = {
            "user_name": request.form.get("user_name"),
            "treatment_name": request.form.get("treatment_name"),
            "treatment_description": request.form.get("treatment_description"),
            "is_urgent": is_urgent,
            "due_date": request.form.get("due_date"),
            "created_by": session["user"]
        }
        mongo.db.treatments.update({"_id": ObjectId(treatment_id)}, submit)
        flash("treatment Successfully Updated")

    treatment = mongo.db.treatments.find_one({"_id": ObjectId(treatment_id)})
    users = mongo.db.users.find().sort("user_name", 1)
    return render_template("edit_treatment.html", treatment=treatment, users=users)


@app.route("/delete_treatment/<treatment_id>")
def delete_treatment(treatment_id):
    mongo.db.treatments.remove({"_id": ObjectId(treatment_id)})
    flash("treatment Successfully Deleted")
    return redirect(url_for("get_treatments"))


@app.route("/get_users")
def get_users():
    users = list(mongo.db.users.find().sort("user_name", 1))
    return render_template("users.html", users=users)


@app.route("/add_user", methods=["GET", "POST"])
def add_user():
    if request.method == "POST":
        user = {
            "user_name": request.form.get("user_name")
        }
        mongo.db.users.insert_one(user)
        flash("New user Added")
        return redirect(url_for("get_users"))

    return render_template("add_user.html")


@app.route("/edit_user/<user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    if request.method == "POST":
        submit = {
            "user_name": request.form.get("user_name")
        }
        mongo.db.users.update({"_id": ObjectId(user_id)}, submit)
        flash("user Successfully Updated")
        return redirect(url_for("get_users"))

    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    return render_template("edit_user.html", user=user)


@app.route("/delete_user/<user_id>")
def delete_user(user_id):
    mongo.db.users.remove({"_id": ObjectId(user_id)})
    flash("user Successfully Deleted")
    return redirect(url_for("get_users"))
