import os
from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
from werkzeug.utils import secure_filename

UPLOAD_DIR = os.path.join("app", "static", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

app = Flask(
    __name__,
    template_folder="app/templates",
    static_folder="app/static"
)
app.config["UPLOAD_FOLDER"] = UPLOAD_DIR
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024  # 8 MB

ALLOWED = {"png", "jpg", "jpeg", "gif"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED

@app.get("/")
def home():
    return render_template("index.html")

@app.post("/analyze")
def analyze():
    text = request.form.get("text", "").strip()
    file = request.files.get("image")

    image_url = None
    info = {}
    if file and allowed_file(file.filename):
        fname = secure_filename(file.filename)
        save_path = os.path.join(app.config["UPLOAD_FOLDER"], fname)
        file.save(save_path)

        # Carga con Pillow para extraer metadatos simples (demo)
        with Image.open(save_path) as im:
            info = {"format": im.format, "size": im.size, "mode": im.mode}

        image_url = url_for("static", filename=f"uploads/{fname}")

    # Aquí podrías añadir más “modalidades” (audio, video, etc.)
    return render_template("result.html", text=text, image_url=image_url, info=info)

if __name__ == "__main__":
    app.run(debug=True)
