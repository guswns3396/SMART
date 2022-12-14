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

    def get_answer(self, answer: int, config: list):
        newconfig = Study.get_answer(self, answer, config)
        self.changed()
        return newconfig


class Subjects(db.Model):
    id = db.Column(db.Text, primary_key=True)


class Studies(db.Model):
    id = db.Column(db.Text, primary_key=True)
    study = db.Column(MutableStudy.as_mutable(db.PickleType), nullable=False)
    numlvls = db.Column(db.Integer, nullable=False)
    p = db.Column(db.Float, nullable=False)
    token = db.Column(db.Text, nullable=False)
    username_field = db.Column(db.Text, nullable=False)
    password_field = db.Column(db.Text, nullable=False)


# class Nodes(db.Model):
#     id = db.Column(db.Integer, autoincrement=True, primary_key=True)
#     parent = db.Column(db.Integer)
#     a = db.Column(db.Integer)
#     b = db.Column(db.Integer)
#     count = db.Column(db.Integer)
#
#     isX = db.Column(db.Boolean, nullable=False)
#     txt = db.Column(db.Text)
#     qset = db.Column(MutableList.as_mutable(db.PickleType))
#
#
# class StudyNodes(db.Model):
#     study_id = db.Column(db.Text, db.ForeignKey('studies.id'), primary_key=True)
#     node_id = db.Column(db.Text, db.ForeignKey('Nodes.id'), primary_key=True)
#
#     study = db.relationship('Studies', backref='studynodes')
#     node = db.relationship('Nodes', backref='nodestudies')
#
#
# class Roots(db.Model):
#     study_id = db.Column(db.Text, db.ForeignKey('studies.id'), primary_key=True)
#     node_id = db.Column(db.Text, db.ForeignKey('Nodes.id'), primary_key=True)
#
#     study = db.relationship('Studies', backref='root')
#     node = db.relationship('Nodes', backref='root')


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
    question_num = db.Column(db.Integer, nullable=False)  # primary question => question_num = 0
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

    answer = db.Column(db.Text, nullable=False)

    subject = db.relationship('Subjects', backref='answers')
    question = db.relationship('Questions', backref='answers')


class Participations(db.Model):
    subject_id = db.Column(db.Text, db.ForeignKey('subjects.id'), primary_key=True)
    study_id = db.Column(db.Text, db.ForeignKey('studies.id'), primary_key=True)

    configuration = db.Column(MutableList.as_mutable(db.PickleType), nullable=False)

    subject = db.relationship('Subjects', backref='participations')
    study = db.relationship('Studies', backref='participations')
