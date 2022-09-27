from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Studies(db.Model):
    id = db.Column(db.Text, primary_key=True)
    study = db.Column(db.PickleType, nullable=False)
