from milestone3 import db

class Therapist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    therapist_name = db.Column(db.String(25), unique=True, nullable=False)
    clients = db.relationship("Client", backref="therapist", cascade="all, delete", lazy=True)
    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return self.therapist_name


class Client(db.Model):
    # schema for the Client model
    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(25), unique=True, nullable=False)
    client_dob = db.Column(db.Date, nullable=False)
    client_email = db.Column(db.String(30), nullable=False)
    client_contact_num = db.Column(db.Integer, nullable=False)
    client_emerg_con_name = db.Column(db.String(40), nullable=False)
    client_emerg_con_num = db.Column(db.Integer, nullable=False)
    client_emerg_rel = db.Column(db.String(25), nullable=False)
    client_contraindications = db.Column(db.Text, nullable=False)
    client_signature = db.Column(db.Boolean, default=False, nullable=False)
    treatments = db.relationship("Treatment", backref="client", cascade="all, delete", lazy=True)
    therapist_id = db.Column(db.Integer, db.ForeignKey("therapist.id", ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return self.client_name


class Treatment(db.Model):
    # schema for the Treatment model
    id = db.Column(db.Integer, primary_key=True)
    treatment_name = db.Column(db.String(50), unique=True, nullable=False)
    treatment_description = db.Column(db.Text, nullable=False)
    required_followup = db.Column(db.Boolean, default=False, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
      
    treatment_observation = db.Column(db.Text, nullable=False)
    treatment_palpation = db.Column(db.Text, nullable=False)
    treatment_muscle_tests = db.Column(db.Text, nullable=False)
    treatment_special_tests = db.Column(db.Text, nullable=False)

    client_id = db.Column(db.Integer, db.ForeignKey("client.id", ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return "#{0} - Treatment: {1} | Required Follow up: {2}".format(
            self.id, self.treatment_name, self.required_followup
        )


class Users(db.Model):
    # schema for the Task model
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(260), nullable=False)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return self.user_name
