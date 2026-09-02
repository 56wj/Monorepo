import os

from flask import Flask, send_from_directory

from path_utils import get_static_images_dir


app = Flask(__name__)
images_directory = get_static_images_dir()


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/images/<path:filename>")
def serve_image(filename):
    return send_from_directory(images_directory, filename)


if __name__ == "__main__":
    os.makedirs(images_directory, exist_ok=True)
    app.run(host="0.0.0.0", port=int(os.getenv("ASSET_SERVER_PORT", "5001")))
