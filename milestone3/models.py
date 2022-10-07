from milestone3 import db


class Client(db.Model):
    # schema for the Client model
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(25), unique=True, nullable=False)
    treatments = db.relationship("Treatment", backref="client", cascade="all, delete", lazy=True)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return self.client_name


class Treatment(db.Model):
    # schema for the Treatment model
    id = db.Column(db.Integer, primary_key=True)
    treatment_name = db.Column(db.String(50), unique=True, nullable=False)
    treatment_description = db.Column(db.Text, nullable=False)
    is_urgent = db.Column(db.Boolean, default=False, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey("client.id", ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return "#{0} - Treatment: {1} | Urgent: {2}".format(
            self.id, self.treatment_name, self.is_urgent
        )


class Users(db.Model):
    # schema for the Task model
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(260), nullable=False)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return self.user_name
