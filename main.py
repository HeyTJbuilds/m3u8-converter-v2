from flask import Flask, request, jsonify
import os
import subprocess
import uuid

app = Flask(__name__)

@app.route('/convert', methods=['POST'])
def convert_m3u8_to_mp3():
    try:
        m3u8_link = request.json.get('m3u8_link')
        if not m3u8_link:
            return jsonify({"error": "No M3U8 link provided"}), 400

        # Generate unique file name
        filename = f"{uuid.uuid4().hex}.mp3"
        output_path = f"/tmp/{filename}"

        # Run ffmpeg command
        subprocess.run([
            "ffmpeg", "-i", m3u8_link, "-vn", "-acodec", "libmp3lame",
            "-ab", "128k", output_path
        ], check=True)

        # Return the file name
        return jsonify({"message": "Conversion successful", "filename": filename}), 200

    except subprocess.CalledProcessError:
        return jsonify({"error": "Error during conversion"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
