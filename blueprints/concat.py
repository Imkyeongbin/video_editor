from flask import request, jsonify
from models import db, ConcatRequest
from . import concat_bp

@concat_bp.route('/concat', methods=['POST'])
def concat_videos():
    data = request.json
    video_ids = data.get('video_ids')

    if not video_ids or len(video_ids) < 2:
        return jsonify({"error": "At least two video IDs are required"}), 400

    concat_request = ConcatRequest(video_ids=','.join(video_ids))
    db.session.add(concat_request)
    db.session.commit()

    return jsonify({"message": "Concat request added"}), 201
