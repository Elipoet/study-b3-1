from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

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
migrate = Migrate(app, db)

# creation form class
class PasswordForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password_hash = PasswordField("Mot de Passe", validators=[DataRequired()])
    submit = SubmitField("Soumettre")

# creation form class
class NamerForm(FlaskForm):
    name = StringField("Nom de l'Utilisateur", validators=[DataRequired()])
    submit = SubmitField("Soumettre")

# creation form user
class UserForm(FlaskForm):
    name = StringField("Nom de l'Utilisateur", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    password_hash = PasswordField("Mot de Passe", validators=[DataRequired(), EqualTo('password_hash2', message="Les mots de passes doivent correspondre")])
    password_hash2 = PasswordField("Confirmer Mot de Passe", validators=[DataRequired()])
    submit = SubmitField("Soumettre")

# Modele db
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(300), nullable=False)

    @property
    def password(self):
        raise AttributeError("Le mot de passe n'est pas une valeur visible")
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Creation String
    def __repr_(self):
        return '<Name %r>' % self.name
    
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

# Listes de Utilisateurs
@app.route('/users')
def users():
    users = Users.query.order_by(Users.id)
    return render_template('users.html', users=users)
# # Creation Page Utilisateurs
# @app.route('/users', methods=['GET', 'POST'])
# def users():
#     name = None
#     form = NamerForm()
#     if form.validate_on_submit():
#         name = form.name.data
#         form.name.data = ''
#         flash("Ajout de l'Utilisateur réussi")
#     return render_template("users.html",
#                            name = name, 
#                            form = form)

@app.route('/user/ajout', methods=['GET','POST'])
def ajout():
    name = None
    form=UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            hashed_password = generate_password_hash(form.password_hash.data, method='pbkdf2')
            user = Users(name=form.name.data, email=form.email.data, password_hash=hashed_password)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.name.data = ''
        form.email.data = ''
        form.password_hash.data = ''
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
        name_to_update.password_hash = request.form['password_hash']
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
                                name_to_update = name_to_update,
                                id = id)

@app.route('/supprimer/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name = None
    form = UserForm()

    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("Suppression Utilisation réussie")
        our_users = Users.query.order_by(Users.date_added)
        return render_template("ajout_utilisateur.html", 
                            name = name,
                            form = form, 
                            our_users = our_users)
    except:
        flash("La supression de l'utilisateur n'a pas fonctionné")
        return render_template("ajout_utilisateur.html", 
                            name = name,
                            form = form, 
                            our_users = our_users)

@app.route('/test_pwd', methods=['GET','POST'])
def test_pwd():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data
        form.email.data = ''
        form.password_hash.data = ''

        pw_to_check = Users.query.filter_by(email=email).first()

        passed = check_password_hash(pw_to_check.password_hash, password)

    return render_template("test_pwd.html",
                           email = email,
                           password = password,
                           pw_to_check = pw_to_check,
                           passed = passed, 
                           form = form)


if __name__ == '__main__':
    app.run(debug=True)