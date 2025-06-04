from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import os
import subprocess
import platform

app = Flask(__name__)
CORS(app)

@app.route("/download", methods=["POST"])
def download():
    data = request.get_json()
    url = data.get("url")
    quality = data.get("quality", "720p")
    format_type = data.get("format", "mp4")

    if not url:
        return jsonify({"error": "Missing YouTube URL"}), 400

    os.makedirs("downloads", exist_ok=True)

    if format_type == "mp3":
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": "downloads/%(title)s.%(ext)s",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        }
    else:
        ydl_opts = {
            "format": f"bestvideo[height<={quality[:-1]}]+bestaudio/best/best",
            "outtmpl": "downloads/%(title)s.%(ext)s",
        }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return jsonify({"message": f"Downloaded as {format_type.upper()} successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)