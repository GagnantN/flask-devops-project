import json
from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)
VIDEO_FILE = "videos.json"

def load_videos():
    try:
        with open(VIDEO_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_videos(videos):
    with open(VIDEO_FILE, "w", encoding="utf-8") as f:
        json.dump(videos, f, indent=4, ensure_ascii=False)

videos = load_videos()

# --- Accueil ---
@app.route("/")
def home():
    return render_template("index.html")

# --- Liste des vidéos ---
@app.route("/videos")
def list_videos():
    return render_template("videos.html", videos=videos)

# --- Page détail d'une vidéo ---
@app.route("/videos/<int:id>")
def video_detail(id):
    video = next((v for v in videos if v["id"] == id), None)
    if not video:
        abort(404)
    return render_template("videos.detail.html", video=video)

# --- Formulaire de modification d'une vidéo ---
@app.route("/videos/<int:id>/edit", methods=["GET", "POST"])
def edit_video(id):
    video = next((v for v in videos if v["id"] == id), None)
    if not video:
        abort(404)
    
    if request.method == "POST":
        video["title"] = request.form.get("title", video["title"])
        video["description"] = request.form.get("description", video.get("description", ""))
        video["url"] = request.form.get("url", video.get("url", ""))
        video["theme"] = request.form.get("theme", video.get("theme", ""))
        save_videos(videos)
        return redirect(url_for("video_detail", id=id))
    
    return render_template("video_form.html", video=video)

# --- Ajouter une vidéo ---
@app.route("/videos/add", methods=["GET", "POST"])
def add_video():
    if request.method == "POST":
        new_id = max((v["id"] for v in videos), default=0) + 1
        new_video = {
            "id": new_id,
            "title": request.form.get("title", ""),
            "description": request.form.get("description", ""),
            "url": request.form.get("url", ""),
            "theme": request.form.get("theme", "")
        }
        videos.append(new_video)
        save_videos(videos)
        return redirect(url_for("list_videos"))
    
    return render_template("video_form.html", video=None)

# --- Supprimer une vidéo ---
@app.route("/videos/<int:id>/delete", methods=["POST"])
def delete_video(id):
    video = next((v for v in videos if v["id"] == id), None)
    if not video:
        abort(404)
    videos.remove(video)
    save_videos(videos)
    return redirect(url_for("list_videos"))

# --- Recherche ---
@app.route("/videos/search", methods=["GET", "POST"])
def search_video():
    results = []
    query = ""
    if request.method == "POST":
        query = request.form.get("query", "")
        results = [v for v in videos if query.lower() in v["title"].lower()]
    return render_template("video_search.html", results=results, query=query)

if __name__ == "__main__":
    app.run(debug=True)
