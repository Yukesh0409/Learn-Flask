from flask import Flask, redirect, url_for,render_template,request,session,flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from notmain import notmainBlueprint


app = Flask("__name__")
app.secret_key = "Yukesh"
app.permanent_session_lifetime = timedelta(minutes=5)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.register_blueprint(notmainBlueprint,url_prefix = "/admin")

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id",db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self,name,email):
        self.name = name
        self.email = email

@app.route("/")
def home():
    return render_template("inheritance.html",name="Yukesh")

@app.route("/<name>")
def testname(name):
    return f"Hello {name}"

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        nameis = request.form["nm"]
        session["user"] = nameis
        user =users.query.filter_by(name = nameis).first()
        if user:
            session["email"] = user.email
        else:
            usr = users(nameis,None)
            db.session.add(usr)
            db.session.commit()

        flash("You have logged in successfully")
        # return redirect(url_for("testname",name=nameis))
        return redirect(url_for("user"))
    else:    
        if "user" in session:
            flash("Already Logged in")
            return redirect(url_for("user"))
        return render_template("login.html")
    
@app.route("/logout")    
def logout():
    session.pop("user",None)
    session.pop("email",None)
    return redirect(url_for("login"))

@app.route("/user",methods=["POST","GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]
        if request.method == "POST":
            flash("Email entered")
            session["email"]=request.form["email"]
            email = session["email"]
            found_user =  users.query.filter_by(name = user).first()
            found_user.email = email
            db.session.commit()
        else:
            if "email" in session:
                email = session["email"]
        return render_template("user.html",email=email)
    else:
        return redirect(url_for("login"))



@app.route("/admin")
def admin():
    return redirect(url_for("testname",name="to home page"))

@app.route("/view")
def view():
    return render_template("view.html", values = users.query.all())

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)