import json
from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)
VIDEO_FILE = "videos.json"

# --- Fonctions utilitaires pour charger et sauvegarder les vidéos ---
def load_videos():
    try:
        with open(VIDEO_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_videos(videos):
    with open(VIDEO_FILE, "w", encoding="utf-8") as f:
        json.dump(videos, f, indent=4, ensure_ascii=False)

# Charger les vidéos au démarrage
videos = load_videos()

# --- Routes ---

@app.route("/")
def home():
    # template index.htm
    return render_template("index.html")

@app.route("/videos")
def list_videos():
    # template videos.html pour la liste
    return render_template("videos.html", videos=videos)

@app.route("/videos/<int:id>", methods=["GET", "POST"])
def video_detail(id):
    # template videos.details.html pour le détail
    video = next((v for v in videos if v["id"] == id), None)
    if not video:
        abort(404, "Vidéo non trouvée")

    if request.method == "POST":
        method = request.form.get("_method")
        if method == "PUT":
            video["title"] = request.form.get("title", video["title"])
            video["description"] = request.form.get("description", video["description"])
            save_videos(videos)
            return redirect(url_for("video_detail", id=id))
        elif method == "DELETE":
            videos.remove(video)
            save_videos(videos)
            return redirect(url_for("list_videos"))

    return render_template("videos.details.html", video=video)

@app.route("/videos/add", methods=["GET", "POST"])
def add_video():
    if request.method == "POST":
        new_id = max((v["id"] for v in videos), default=0) + 1
        new_video = {
            "id": new_id,
            "title": request.form["title"],
            "description": request.form["description"],
            "views": 0
        }
        videos.append(new_video)
        save_videos(videos)
        return redirect(url_for("list_videos"))
    # On peut réutiliser videos.details.html pour le formulaire si tu veux,
    # sinon il faut créer videos.add.html
    return render_template("videos.details.html", video=None)

@app.route("/videos/search", methods=["GET", "POST"])
def search_video():
    results = []
    query = ""
    if request.method == "POST":
        query = request.form.get("query", "")
        results = [v for v in videos if query.lower() in v["title"].lower()]
    # On peut réutiliser videos.html pour afficher les résultats
    return render_template("videos.html", videos=results)

# --- Démarrage de l'application ---
if __name__ == "__main__":
    app.run(debug=True)
