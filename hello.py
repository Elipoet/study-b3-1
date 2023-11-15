from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired

# creation flask instance
app = Flask(__name__)
# creation secret key
app.config['SECRET_KEY'] = "secretkey_studi_b3"


# creation form class
class NamerForm(FlaskForm):
    name = StringField("Nom de l'Utilisateur", validators=[DataRequired()])
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

    return render_template("users.html",
                           name = name, 
                           form = form)

if __name__ == '__main__':
    app.run(debug=True)