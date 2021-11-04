from flask import request, render_template, make_response
from flask import current_app as app
from .models import db, Person

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

    return json.dumps({'pid':pid})