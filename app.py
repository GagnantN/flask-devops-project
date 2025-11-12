import json
from flask import Flask, render_template, request, redirect, url_for, abort

# Création de l'application Flask
app = Flask(__name__)

# Nom du fichier JSON où les vidéos sont stockées
VIDEO_FILE = "videos.json"

# ---------------------- Fonctions utilitaires ------------------------
def load_videos():
    """
    Charge la liste des vidéos depuis le fichier JSON.
    Si le fichier n'existe pas, retourne une liste vide.
    """

    try:
        with open(VIDEO_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []



def save_videos(videos):
    """
    Sauvegarde la liste des vidéos dans le fichier JSON.
    """

    with open(VIDEO_FILE, "w", encoding="utf-8") as f:
        json.dump(videos, f, indent=4, ensure_ascii=False)
        # 'indent=4' pour avoir un JSON lisible, 'ensure_ascii=False' pour garder les caractères spéciaux

# Charger les vidéos au démarrage
videos = load_videos()


# ----------------------------- Accueil -------------------------------
'''
Route de la page d'accueil'''
@app.route("/")
def home():
    return render_template("index.html")


# ------------------------- Liste des vidéos --------------------------
'''
Route pour afficher toutes les vidéos
Passe la liste 'videos' au template
'''

@app.route("/videos")
def list_videos():
    return render_template("videos.html", videos=videos)


# ---------------------- Page détail d'une vidéo ----------------------
'''
Route pour afficher les details d'une vidéo spécifique
<int:id> : récupère l'ID de la vidéo depuis l'URL
'''
@app.route("/videos/<int:id>")
def video_detail(id):
    # Cherche la vidéo correspondant à l'ID
    video = next((v for v in videos if v["id"] == id), None)

    if not video:
        abort(404) # Si la vidéo n'existe pas, renvoie une erreur 404

    # Passe la vidéo au template pour affichage
    return render_template("videos.detail.html", video=video)



# ------------------- Formulaire modification vidéo -------------------
'''
Route pour modifier une vidéo existante.
GET : affiche le formulaire pré-rempli
POST : récupère les données et met à jour la vidéo
'''

@app.route("/videos/<int:id>/edit", methods=["GET", "POST"])
def edit_video(id):
    # Cherche la vidéo à modifier
    video = next((v for v in videos if v["id"] == id), None)
    if not video:
        abort(404)
    
    if request.method == "POST":
        # Récupère les champs du formulaire et met à jour la vido
        video["title"] = request.form.get("title", video["title"])
        video["description"] = request.form.get("description", video.get("description", ""))
        video["url"] = request.form.get("url", video.get("url", ""))
        video["theme"] = request.form.get("theme", video.get("theme", ""))

        # Sauvegarde la liste mise à jour dans le JSON
        save_videos(videos)

        # Redirige vers la page détail de la vidéo modifiée
        return redirect(url_for("video_detail", id=id))
    
    # Si GET, affiche le formulaire pré-rempli
    return render_template("video_form.html", video=video)



# ------------------------- Ajouter une vidéo -------------------------
'''
oute pour ajouter une nouvelle vidéo.
GET : affiche le formulaire vide
POST : récupère les données et crée une nouvelle vidéo
'''

@app.route("/videos/add", methods=["GET", "POST"])
def add_video():
    if request.method == "POST":
        # Création d'un nouvel ID unique
        new_id = max((v["id"] for v in videos), default=0) + 1

        # Création de la nouvelle vidéo avec les données du formulaire
        new_video = {
            "id": new_id,
            "title": request.form.get("title", ""),
            "description": request.form.get("description", ""),
            "url": request.form.get("url", ""),
            "theme": request.form.get("theme", "")
        }

        # Ajoute la vidéo à la liste
        videos.append(new_video)
        save_videos(videos) # Sauvegarde la liste mise à jour

        # Redirige vers la liste des vidéos
        return redirect(url_for("list_videos"))
    
    # Si GET, affiche juste le formulaire vide
    return render_template("video_form.html", video=None)



# -------------------------- Supprimer vidéo --------------------------
@app.route("/videos/<int:id>/delete", methods=["POST"])
def delete_video(id):
    '''
    Route pour supprimer une vidéo.
    Se déclenche via un formulaire POST pour éviter la suppression par URL directe.
    '''

    # Cherche la vidéo à supprimer
    video = next((v for v in videos if v["id"] == id), None)
    if not video:
        abort(404)

    # Supprime la vidéo de la liste
    videos.remove(video)
    save_videos(videos) # Sauvegarde la liste mise à jour

    # Redirige vers la liste des vidéos
    return redirect(url_for("list_videos"))


# ----------------------------- Rechercher ----------------------------
@app.route("/videos/search", methods=["GET", "POST"])
def search_video():
    '''
    Route pour rechercher une vidéo par titre.
    GET : affiche le formulaire de recherche vide
    POST : récupère la requête et affiche les résultats
    '''

    results = []
    query = ""

    if request.method == "POST":
        query = request.form.get("query", "")
        # Filtre les vidéos dont le titre contient la requête
        results = [v for v in videos if query.lower() in v["title"].lower()]

    return render_template("video_search.html", results=results, query=query)



# ------------------------ Lancer l'application -----------------------
if __name__ == "__main__":
    # Lancement du serveur Flask en mode debug
    app.run(debug=True)
