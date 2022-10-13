from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.mutable import Mutable
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


class Studies(db.Model):
    id = db.Column(db.Text, primary_key=True)
    study = db.Column(MutableStudy.as_mutable(db.PickleType), nullable=False)
