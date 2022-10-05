import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from milestone3 import app, db
from milestone3.models import Client, Treatment
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env


app2 = Flask(__name__)


app2.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app2.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app2.secret_key = os.environ.get("SECRET_KEY")


mongo = PyMongo(app2)


@app.route("/")
def home():
    treatments = list(Treatment.query.order_by(Treatment.id).all())
    return render_template("treatments.html", treatments=treatments)


@app.route("/clients")
def clients():
    clients = list(Client.query.order_by(Client.client_name).all())
    return render_template("clients.html", clients=clients)


@app.route("/add_client", methods=["GET", "POST"])
def add_client():
    if request.method == "POST":
        client = Client(client_name=request.form.get("client_name"))
        db.session.add(client)
        db.session.commit()
        return redirect(url_for("clients"))
    return render_template("add_client.html")


@app.route("/edit_client/<int:client_id>", methods=["GET", "POST"])
def edit_client(client_id):
    client = Client.query.get_or_404(client_id)
    if request.method == "POST":
        client.client_name = request.form.get("client_name")
        db.session.commit()
        return redirect(url_for("clients"))
    return render_template("edit_client.html", client=client)


@app.route("/delete_client/<int:client_id>")
def delete_client(client_id):
    client = Client.query.get_or_404(client_id)
    db.session.delete(client)
    db.session.commit()
    return redirect(url_for("clients"))


@app.route("/add_treatment", methods=["GET", "POST"])
def add_treatment():
    clients = list(Client.query.order_by(Client.client_name).all())
    if request.method == "POST":
        treatment = Treatment(
            treatment_name=request.form.get("treatment_name"),
            treatment_description=request.form.get("treatment_description"),
            is_urgent=bool(True if request.form.get("is_urgent") else False),
            due_date=request.form.get("due_date"),
            client_id=request.form.get("client_id"))
        db.session.add(treatment)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add_treatment.html", clients=clients)


@app.route("/edit_treatment/<int:treatment_id>", methods=["GET", "POST"])
def edit_treatment(treatment_id):
    treatment = Treatment.query.get_or_404(treatment_id)
    clients = list(Client.query.order_by(Client.client_name).all())
    if request.method == "POST":
        treatment.treatment_name = request.form.get("treatment_name")
        treatment.treatment_description = request.form.get("treatment_description")
        treatment.is_urgent = bool(True if request.form.get("is_urgent") else False)
        treatment.due_date = request.form.get("due_date")
        treatment.client_id = request.form.get("client_id")
        db.session.commit()
    return render_template("edit_treatment.html", treatment=treatment, clients=clients)


@app.route("/delete_treatment/<int:treatment_id>")
def delete_treatment(treatment_id):
    treatment = Treatment.query.get_or_404(treatment_id)
    db.session.delete(treatment)
    db.session.commit()
    return redirect(url_for("home"))