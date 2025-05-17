from flask import Flask, render_template, request, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

DOWNLOADS_DIR = "downloads"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form['youtube_url']
    if not url:
        return "URL inválida", 400

    # Nombre aleatorio para evitar colisiones
    filename = f"{uuid.uuid4()}.mp3"
    output_path = os.path.join(DOWNLOADS_DIR, filename)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
    except Exception as e:
        return f"Error al descargar el video: {str(e)}", 500

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    os.makedirs(DOWNLOADS_DIR, exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
