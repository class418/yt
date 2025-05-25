from flask import Flask, request, jsonify, render_template
from yt_dlp import YoutubeDL
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_video_url', methods=['POST'])
def get_video_url():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'error': 'URLがありません'}), 400

    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'skip_download': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            video_url = info['url']
            return jsonify({'video_url': video_url})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
