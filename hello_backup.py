from flask import Flask, render_template, flash, request, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager, login_required, logout_user, current_user, login_user

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
    name = StringField("Nom Prénom", validators=[DataRequired()])
    username = StringField("Nom d'Utilisateur", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    password_hash = PasswordField("Mot de Passe", validators=[DataRequired(), EqualTo('password_hash2', message="Les mots de passes doivent correspondre")])
    password_hash2 = PasswordField("Confirmer Mot de Passe", validators=[DataRequired()])
    submit = SubmitField("Soumettre")

# Flask_login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# Create Login Form
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Mot de Passe", validators=[DataRequired()])
    submit = SubmitField("Soumettre")

# Modele db
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
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
            user = Users(username=form.username.data, name=form.name.data, email=form.email.data, password_hash=hashed_password)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        form.username.data = ''
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
# changement de pwd ne fonctionne plus !
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.username = request.form['username']
        try:
            db.session.commit()
            flash("Mise à Jour Utilisateur réussie")
            return render_template("update.html",
                                   form = form,
                                   name_to_update = name_to_update,
                                   id=id)
        except: 
            flash("Erreur ! Essayez de nouveau.")
            return render_template("update.html",
                                   form = form,
                                   name_to_update = name_to_update,
                                   id=id)
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
        flash("Suppression Utilisateur réussie")
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

# login page
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("La connexion a réussi.")
                return redirect(url_for('dashboard'))
            else : 
                flash("La connexion n'a pas réussi. Le nom d'utilisateur ou mot de passe ne correspondent pas.")
                return render_template('login.html', form=form)
        else : 
            flash("Ce nom d'utilisateur n'existe pas.")
    return render_template('login.html', form=form)

# logout page
@app.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    flash("Vous avez été déconnecté.")
    return redirect(url_for('login'))

# Dashboard page
@app.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    form = UserForm()
    id = current_user.id
    # changement de pwd ne fonctionne plus !
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.username = request.form['username']
        try:
            db.session.commit()
            flash("Mise à Jour Utilisateur réussie")
            return render_template("dashboard.html",
                                form = form,
                                name_to_update = name_to_update,
                                id=id)
        except: 
            flash("Erreur ! Essayez de nouveau.")
            return render_template("dashboard.html",
                                form = form,
                                name_to_update = name_to_update,
                                id=id)
    else:
        return render_template("dashboard.html",
                                form = form,
                                name_to_update = name_to_update,
                                id=id)
if __name__ == '__main__':
    app.run(debug=True)