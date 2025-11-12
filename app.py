import json
from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)
VIDEO_FILE = "videos.json"

# --- Fonctions pour lire et écrire les vidéos ---
def load_videos():
    try:
        with open(VIDEO_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_videos(videos):
    with open(VIDEO_FILE, "w", encoding="utf-8") as f:
        json.dump(videos, f, indent=4, ensure_ascii=False)

# --- Charger les vidéos au démarrage ---
videos = load_videos()

# --- Route GET / : page d'accueil ---
@app.route("/")
def home():
    return render_template("index.html")

# --- Route GET /videos : afficher toutes les vidéos ---
@app.route("/videos")
def list_videos():
    return render_template("videos.html", videos=videos)

# --- Route GET/PUT/DELETE /videos/<int:id> ---
@app.route("/videos/<int:id>", methods=["GET", "POST"])
def video_detail(id):
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

    return render_template("videos.detail.html", video=video)

# --- Route GET /videos/add : afficher formulaire ---
# --- Route POST /videos/add : ajouter la vidéo ---
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
    return render_template("video_form.html")

# --- Route GET /videos/search : rechercher par titre ---
@app.route("/videos/search", methods=["GET", "POST"])
def search_video():
    results = []
    query = ""
    if request.method == "POST":
        query = request.form.get("query", "")
        results = [v for v in videos if query.lower() in v["title"].lower()]
    return render_template("video_search.html", results=results, query=query)

# --- Démarrage de l'application ---
if __name__ == "__main__":
    app.run(debug=True)
