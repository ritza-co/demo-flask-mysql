from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from json import JSONEncoder
import json
import os

app = Flask(__name__, instance_relative_config=False)

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ECHO"] = False
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# db variable initialization
db = SQLAlchemy(app)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    surname = db.Column(db.String(60))

    def __repr__(self):
        return '<Person: {}>'.format(self.name)

db.init_app(app)
db.create_all()  # Create sql tables for our data models

class PersonEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/signUp',methods=['POST'])
def signUp():

    # read the posted values from the UI
    name = request.form['name']
    surname = request.form['surname']

    person = Person(name = name, surname = surname )

    db.session.add(person)
    db.session.flush()

    pid = person.id
    print(pid)
    db.session.commit()

    return jsonify({'pid':pid})
    
    # # validate the received values
    # if name and surname:
    #     return json.dumps({'html':'<span>All fields good !!</span>'})
    # else:
    #     return json.dumps({'html':'<span>Enter the required fields</span>'})

@app.route('/view',methods=['POST'])
def view():
    pid = request.json['pid']
    print("The view pid: ", pid)

    person = Person.query.filter_by(id=pid)
    print("The view person: ", person)

    personJSONData = json.dumps(person, indent=4, cls=PersonEncoder)

    return personJSONData

if __name__ == "__main__":
    app.run()