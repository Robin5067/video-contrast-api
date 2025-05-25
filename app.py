from flask import Flask, request, send_file
import subprocess
import requests

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process_video():
    data = request.json
    video_url = data.get("video_url")

    if not video_url:
        return {"error": "No video_url provided"}, 400

    input_file = "input.mp4"
    output_file = "output.mp4"

    response = requests.get(video_url)
    with open(input_file, "wb") as f:
        f.write(response.content)

    subprocess.run([
        "ffmpeg", "-i", input_file, "-vf", "eq=contrast=1.3", output_file
    ])

    return send_file(output_file, as_attachment=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)