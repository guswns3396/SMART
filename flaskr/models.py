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


class Subjects(db.Model):
    id = db.Column(db.Text, primary_key=True)


class Studies(db.Model):
    id = db.Column(db.Text, primary_key=True)
    study = db.Column(MutableStudy.as_mutable(db.PickleType), nullable=False)
    token = db.Column(db.Text, nullable=False)
    username_field = db.Column(db.Text, nullable=False)
    password_field = db.Column(db.Text, nullable=False)


class Levels(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    level_num = db.Column(db.Integer, nullable=False)
    scna = db.Column(db.Text)
    scnb = db.Column(db.Text)


# turn into table
class StudyLevels(db.Model):
    level_id = db.Column(db.Integer, db.ForeignKey('levels.id'), primary_key=True)
    study_id = db.Column(db.Text, db.ForeignKey('studies.id'), primary_key=True)

    level = db.relationship('Levels', backref='levelstudies')
    study = db.relationship('Studies', backref='studylevels')


class Questions(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    question_num = db.Column(db.Integer, nullable=False)  # primary question => question_num = 1
    question = db.Column(db.Text, nullable=False)
    range = db.Column(MutableDict.as_mutable(db.PickleType), nullable=False)


# turn into table
class LevelQuestions(db.Model):
    level_id = db.Column(db.Integer, db.ForeignKey('levels.id'), primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), primary_key=True)

    level = db.relationship('Levels', backref='levelquestions')
    question = db.relationship('Questions', backref='questionlevels')


class Answers(db.Model):
    subject_id = db.Column(db.Text, db.ForeignKey('subjects.id'), primary_key=True)
    question_id = db.Column(db.Text, db.ForeignKey('questions.id'), primary_key=True)

    answer = db.Column(MutableDict.as_mutable(db.PickleType), nullable=False)

    subject = db.relationship('Subjects', backref='answers')
    question = db.relationship('Questions', backref='answers')


class Participations(db.Model):
    subject_id = db.Column(db.Text, db.ForeignKey('subjects.id'), primary_key=True)
    study_id = db.Column(db.Text, db.ForeignKey('studies.id'), primary_key=True)

    configuration = db.Column(MutableList.as_mutable(db.PickleType), nullable=False)

    subject = db.relationship('Subjects', backref='participations')
    study = db.relationship('Studies', backref='participations')
