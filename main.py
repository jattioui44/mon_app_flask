from flask import Flask , render_template , request ,redirect , url_for ,session 
import datetime
app = Flask(__name__)
app.secret_key = "940bdc12afa81f9b0bb407b1640bb843fe51c398be2e281d3088f7125baf66a5"
# pour générer un clé scret dans python 
#  import secrets
#  secrets.token_hex()
# app.secret_key = "5208a3ddf27435a79ad5eb0f5ddeb70ad42602fa7f3f5b161bb7d390280fc990"
@app.route('/')
def index():
    return render_template("index.html")
@app.route('/heure')
def heure():
    date=datetime.datetime.now()
    h=date.hour
    m=date.minute
    s=date.second
    return render_template("heure.html", heure=h, minute=m, seconde=s)

liste_eleves=[
    {'nom':'Jattioui','prenom':'mohammed','classe':'2A'},
    {'nom':'Jattioui','prenom':'Hamza','classe':'2B'},
    {'nom':'el alouche','prenom':'mohammed','classe':'TC'},
    {'nom':'el alouche','prenom':'said','classe':'2A'}
]
@app.route('/eleve')
def eleves():
    # print(request.args)
    # print(request.args['c'])
    # print(request.args['autre'])
    classe=request.args.get('c')
    if classe:
        eleves_selectionnes =[eleve for eleve in liste_eleves if eleve['classe'] == classe]
    else:
        eleves_selectionnes = [] 
    return render_template("eleves.html",eleves=eleves_selectionnes)
@app.route('/form')
def formulaire():
    return render_template("formulaire.html")

utilisateurs = [
    {'nom':'admin','mdp':'1234'},
    {'nom':'jattioui','mdp':'1234'},
    {'nom':'user','mdp':'user'}
]
def recherche_utilisateur(nom_utilisateur,mot_de_passe):
    for utilisateur in utilisateurs:
        if utilisateur["nom"] == nom_utilisateur and utilisateur['mdp'] == mot_de_passe:
            return utilisateur
    return None
@app.route('/login', methods=["POST","GET"])
def login():
    # print(request.args) Pour la méthode get
    if request.method == "POST" :
        donnees=request.form
        print(donnees)
        nom=donnees.get('nom')
        mdp=donnees.get('mdp')
        print(nom,mdp)
        utilisateur = recherche_utilisateur(nom,mdp)
        if utilisateur is not None:
            print('utilisateur trouvé ')
            session["nom_utilisateur"] = utilisateur['nom']
            return redirect(url_for('index'))
        else:
            return redirect(request.url)
    else:
            if "nom_utilisateur" in session:
                return redirect(url_for('index'))
            return render_template("login.html")
    # return render_template("login.html")
@app.route('/traitment', methods=["POST","GET"])
def traitemment():
    # print(request.args) Pour la méthode get
    if request.method == "POST" :
        donnees=request.form
        print(donnees)
        nom=donnees.get('nom')
        mdp=donnees.get('mdp')
        print(nom,mdp)
        # if nom == 'admin' and mdp=='1234':
        #     return f"Bonjour {nom}, vous êtes connecté !"
        # else:
        #     return "un probléme est survenu. "
        if nom == 'admin' and mdp=='1234':
            return render_template('traitement.html',nom_utilisateur=nom)
        else:
            return render_template('traitement.html')
        # 
    else:
            return redirect(url_for('index'))
    # return  "traitement de données "

@app.route('/compteur')
def compteur():
    if "compteur" not in session:
        session["compteur"] = 1
    else:
        session["compteur"] = session["compteur"] + 1
    nb_visite = session["compteur"]
    return f"vous avez visité cette page {nb_visite} fois. "
if __name__=='__main__':
    app.run(debug=True)