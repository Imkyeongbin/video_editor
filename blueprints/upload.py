from flask import current_app, request, jsonify
from werkzeug.utils import secure_filename
import os
import uuid
from models import db, Video
from . import upload_bp

@upload_bp.route('/upload', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    files = request.files.getlist('file')
    
    if not files or any(file.filename == '' for file in files):
        return jsonify({"error": "No selected file"}), 400

    video_ids = []

    for file in files:
        if file:
            filename = secure_filename(file.filename)
            video_id = str(uuid.uuid4())
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

            video = Video(id=video_id, filename=filename)
            db.session.add(video)
            video_ids.append(video_id)

    db.session.commit()

    return jsonify({"video_ids": video_ids}), 201
