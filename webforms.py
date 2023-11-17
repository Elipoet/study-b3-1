from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from flask_migrate import Migrate
from flask_login import UserMixin, LoginManager, login_required, logout_user, current_user, login_user

# Create Login Form
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Mot de Passe", validators=[DataRequired()])
    submit = SubmitField("Soumettre")
    
# creation form user
class UserForm(FlaskForm):
    name = StringField("Nom Prénom", validators=[DataRequired()])
    username = StringField("Nom d'Utilisateur", validators=[DataRequired()])
    email = EmailField("Email", validators=[DataRequired()])
    password_hash = PasswordField("Mot de Passe", validators=[DataRequired(), EqualTo('password_hash2', message="Les mots de passes doivent correspondre")])
    password_hash2 = PasswordField("Confirmer Mot de Passe", validators=[DataRequired()])
    submit = SubmitField("Soumettre")

# creation form class
class PasswordForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password_hash = PasswordField("Mot de Passe", validators=[DataRequired()])
    submit = SubmitField("Soumettre")

# creation form class
class NamerForm(FlaskForm):
    name = StringField("Nom de l'Utilisateur", validators=[DataRequired()])
    submit = SubmitField("Soumettre")