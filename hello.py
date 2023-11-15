from flask import Flask, render_template

app = Flask(__name__)

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