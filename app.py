from flask import Flask, request, send_file, render_template
import os, uuid, shutil, subprocess

app = Flask(__name__)
DOWNLOADS_FOLDER = "downloads"
os.makedirs(DOWNLOADS_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get Spotify links
        links = []
        if 'file' in request.files and request.files['file'].filename:
            file = request.files['file']
            links = file.read().decode('utf-8').splitlines()
        elif 'links' in request.form:
            links = request.form['links'].splitlines()
        links = [l.strip() for l in links if l.strip()]
        if not links:
            return "No valid Spotify links provided."

        # Create unique folder
        session_id = str(uuid.uuid4())
        download_dir = os.path.join(DOWNLOADS_FOLDER, session_id)
        os.makedirs(download_dir, exist_ok=True)

        # Download each song using spotdl
        for link in links:
            subprocess.run([
                "spotdl", link,
                "--output", f"{download_dir}/"
            ])

        # Zip the folder
        zip_path = f"{download_dir}.zip"
        shutil.make_archive(download_dir, 'zip', download_dir)

        # Send the zipped file
        return send_file(zip_path, as_attachment=True)

    return render_template("index.html")

# Start the Flask server
if __name__ == '__main__':
    app.run(debug=True)
