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