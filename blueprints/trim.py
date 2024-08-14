from flask import request, jsonify
from models import db, TrimRequest
from . import trim_bp

@trim_bp.route('/trim', methods=['POST'])
def trim_video():
    data = request.json
    video_id = data.get('video_id')
    trim_start = data.get('trim_start')
    trim_end = data.get('trim_end')

    if not video_id or not trim_start or not trim_end:
        return jsonify({"error": "Missing parameters"}), 400

    trim_request = TrimRequest(video_id=video_id, trim_start=trim_start, trim_end=trim_end)
    db.session.add(trim_request)
    db.session.commit()

    return jsonify({"message": "Trim request added"}), 201
