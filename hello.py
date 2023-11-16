from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# creation flask instance
app = Flask(__name__)
app.app_context().push()

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:NewPassword0!@localhost/our_users'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# creation secret key
app.config['SECRET_KEY'] = "secretkey_studi_b3"

#Initialisation db
db = SQLAlchemy(app)

# creation form class
class NamerForm(FlaskForm):
    name = StringField("Nom de l'Utilisateur", validators=[DataRequired()])
    submit = SubmitField("Soumettre")


# Modele db
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    # password = db.Column(db.String(100), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    # Creation String
    def __repr_(self):
        return '<Name %r>' % self.name
    
# creation form user
class UserForm(FlaskForm):
    name = StringField("Nom de l'Utilisateur", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    submit = SubmitField("Soumettre")

#Accueil'
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/user/<name>')
def admin(name):
    return render_template("admin.html",
                            name=name)

# Pages Invalides
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Erreur Serveur
@app.errorhandler(500)
def page_not_found(e):
    return render_template("500.html"), 500

# Creation Page Utilisateurs
@app.route('/users', methods=['GET', 'POST'])
def users():
    name = None
    form = NamerForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''
        flash("Ajout de l'Utilisateur réussi")
    return render_template("users.html",
                           name = name, 
                           form = form)

@app.route('/user/ajout', methods=['GET','POST'])
def ajout():
    name = None
    form=UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        flash("Utilisateur ajouté")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("ajout_utilisateur.html", 
                           name = name,
                           form = form, 
                           our_users = our_users)

# MàJ db
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        try:
            db.session.commit()
            flash("Mise à Jours Utilisateur réussie")
            return render_template("update.html",
                                   form = form,
                                   name_to_update = name_to_update)
        except: 
            flash("Erreur ! Essayez de nouveau.")
            return render_template("update.html",
                                   form = form,
                                   name_to_update = name_to_update)
    else:
        return render_template("update.html",
                                form = form,
                                name_to_update = name_to_update)

if __name__ == '__main__':
    app.run(debug=True)