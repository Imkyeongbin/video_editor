from flask import current_app, send_file, jsonify
import os
from models import FinalVideo
from . import download_bp

@download_bp.route('/download/<video_id>', methods=['GET'])
def download_final_video(video_id):
    final_video = FinalVideo.query.filter_by(id=video_id).first()
    if not final_video:
        return jsonify({"error": "Final video not found"}), 404

    filepath = os.path.join(current_app.config['FINAL_FOLDER'], final_video.filename)
    return send_file(filepath, as_attachment=True)
