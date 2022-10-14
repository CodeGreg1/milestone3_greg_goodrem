from milestone3 import db


class Client(db.Model):
    # schema for the Client model
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(25), unique=True, nullable=False)
    client_dob = db.Column(db.Date, nullable=False)
    client_email = db.Column(db.String(30), nullable=False)
    client_phone = db.Column(db.String(15), nullable=False)
    treatments = db.relationship(
        "Treatment", backref="client", cascade="all, delete", lazy=True)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return self.client_name


class Treatment(db.Model):
    # schema for the Treatment model
    id = db.Column(db.Integer, primary_key=True)
    treatment_client = db.Column(db.String(50), unique=True, nullable=False)
    treatment_name = db.Column(db.String(50), unique=True, nullable=False)
    treatment_subjective = db.Column(db.Text, nullable=False)
    follow_up = db.Column(db.Boolean, default=False, nullable=False)
    treatment_date = db.Column(db.Date, nullable=False)
    treatment_observation = db.Column(db.Text, nullable=False)
    treatment_palpation = db.Column(db.Text, nullable=False)
    treatment_rom = db.Column(db.Text, nullable=False)
    treatment_special_tests = db.Column(db.Text, nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey(
        "client.id", ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return "#{0} - Treatment: {1} | Follow Up: {2}".format(
            self.id, self.treatment_name, self.follow_up
        )


class User(db.Model):
    # schema for the Treatment model
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(260), nullable=False)
    fullname = db.Column(db.String(25), unique=True, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    email = db.Column(db.String(30), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    
    def __repr__(self):
        return self.user_name