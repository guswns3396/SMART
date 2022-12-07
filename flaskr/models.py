from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.mutable import Mutable, MutableDict, MutableList
from flaskr.Study import Study

db = SQLAlchemy()


class MutableStudy(Mutable, Study):
    @classmethod
    def coerce(cls, key, value) -> None:
        if not isinstance(value, MutableStudy):
            if isinstance(value, dict):
                return MutableStudy(value)

            # this call will raise ValueError
            return Mutable.coerce(key, value)
        else:
            return value

    def __getstate__(self):
        d = self.__dict__.copy()
        d.pop('_parents', None)
        return d

    def enroll(self):
        Study.enroll(self)
        self.changed()

    def randomize(self, config):
        x = Study.randomize(self, config)
        self.changed()
        return x

    def get_answers(self, answers: 'ImmutableMultiDict', config: list):
        newconfig = Study.get_answers(self, answers, config)
        self.changed()
        return newconfig


# Participations = db.Table(
#     'participations',
#     db.Column('subject', db.Text, db.ForeignKey('subjects.id')),
#     db.Column('study', db.Text, db.ForeignKey('studies.id')),
#     db.Column('configuration', MutableList.as_mutable(db.PickleType), nullable=False)
# )

Answers = db.Table(
    'answers',
    db.Column('subject', db.Text, db.ForeignKey('subjects.id')),
    db.Column('study', db.Text, db.ForeignKey('studies.id')),
    db.Column('answer', MutableDict.as_mutable(db.PickleType))
)


class Studies(db.Model):
    id = db.Column(db.Text, primary_key=True)
    study = db.Column(MutableStudy.as_mutable(db.PickleType), nullable=False)
    token = db.Column(db.Text, nullable=False)
    username_field = db.Column(db.Text, nullable=False)
    password_field = db.Column(db.Text, nullable=False)


class Subjects(db.Model):
    id = db.Column(db.Text, primary_key=True)
    # subject_participations = db.relationship('Studies', secondary=Participations, backref='study_participants')
    # subject_answers = db.relationship('Studies', secondary=Answers, backref='study_answers')

class Participations(db.Model):
    subject = db.Column(db.Text, db.ForeignKey('subjects.id'), primary_key=True)
    study = db.Column(db.Text, db.ForeignKey('studies.id'), primary_key=True)

    configuration = db.Column(MutableList.as_mutable(db.PickleType), nullable=False)

    subject_rel = db.relationship('Subjects', backref='subject_participations')
    study_rel = db.relationship('Studies', backref='study_participants')
