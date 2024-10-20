from flask import Flask, request, redirect, render_template, flash, jsonify, send_file
from contacts_model import Contact
import time

Contact.load_db()

app = Flask(__name__)

@app.route("/")
def index():
    return redirect("/contacts")

@app.route("/contacts")
def contacts():
    search = request.args.get("q")
    if search is not None:
        contacts_set = Contact.search(search)
    else:
        contacts_set = Contact.all()

    return render_template("index.html", contacts=contacts_set)

@app.route("/contacts/new", methods=['GET'])
def contacts_new_get():
    return render_template("new.html", contact=Contact())

@app.route("/contacts/new", methods=['POST'])
def contacts_new():
    c = Contact(None, request.form['first_name'], request.form['last_name'], request.form['phone'], request.form['email'])
    first_name = request.form['first_name']
    if c.save():
        # flash("New Contact Created")
        # redirect("/contacts")
        return render_template("success.html", name=first_name)
    else:
        return render_template("new.html", contact=c)