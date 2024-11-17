from flask import Flask, request, redirect, render_template, flash, jsonify, send_file
from contacts_model import Contact, Archiver
import time

Contact.load_db()

app = Flask(__name__)

@app.route("/")
def index():
    return redirect("/contacts")

@app.route("/contacts")
def contacts():
    search = request.args.get("q")
    page = int(request.args.get("page", 1))
    if search is not None:
        contacts_set = Contact.search(search)
        if request.headers.get('HX-Trigger') == 'search':
            return render_template("rows.html", contacts=contacts_set)
    else:
        contacts_set = Contact.all()

    return render_template("index.html", contacts=contacts_set, page=page, archiver=Archiver.get())

@app.route("/contacts/count")
def contacts_count():
    count = Contact.count()
    return "(" + str(count) + " total Contacts)"

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
    
@app.route("/contacts/<contact_id>/edit", methods=["GET"])
def contacts_edit_get(contact_id=0):
    contact = Contact.find(contact_id)
    return render_template("edit.html", contact=contact)

@app.route("/contacts/<contact_id>/edit", methods=["POST"])
def contacts_edit_post(contact_id=0):
    c = Contact.find(contact_id)
    c.update(request.form['first_name'], request.form['last_name'], request.form['phone'], request.form['email'])
    if c.save():
        return redirect("/contacts" + str(contact_id))
    else:
        return render_template("edit.html", contact=c)
    
@app.route("/contacts/<contact_id>", methods=["DELETE"])
def contacts_delete(contact_id=0):
    contact = Contact.find(contact_id)
    contact.delete()
    return redirect("/contacts", 303)   

@app.route("/contacts/archive", methods=["POST"])
def start_archive():
    archiver = Archiver.get()
    archiver.run()
    return render_template("archive_ui.html", archiver=archiver)


@app.route("/contacts/archive", methods=["GET"])
def archive_status():
    archiver = Archiver.get()
    return render_template("archive_ui.html", archiver=archiver)


@app.route("/contacts/archive/file", methods=["GET"])
def archive_content():
    archiver = Archiver.get()
    return send_file(archiver.archive_file(), "archive.json", as_attachment=True)


@app.route("/contacts/archive", methods=["DELETE"])
def reset_archive():
    archiver = Archiver.get()
    archiver.reset()
    return render_template("archive_ui.html", archiver=archiver)