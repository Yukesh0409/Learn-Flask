from flask import Blueprint,render_template

notmainBlueprint = Blueprint("notmain",__name__, template_folder="templates")

@notmainBlueprint.route("/login")
def login():
    return "<h1>Admin Page</h1>"