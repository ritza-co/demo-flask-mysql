from flask_login import UserMixin
from app import db

class Person(UserMixin, db.Model):
    """
    Create an Person table
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    surname = db.Column(db.String(60))

    def __repr__(self):
        return '<Person: {}>'.format(self.name)