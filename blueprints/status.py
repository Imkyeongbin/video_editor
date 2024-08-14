from flask import jsonify
from models import Video, TrimRequest, ConcatRequest, FinalVideo
from . import status_bp

@status_bp.route('/videos', methods=['GET'])
def list_videos():
    videos = Video.query.all()
    trim_requests = TrimRequest.query.all()
    concat_requests = ConcatRequest.query.all()
    outputs = FinalVideo.query.all()

    return jsonify({
        "videos": [{"id": v.id, "filename": v.filename} for v in videos],
        "trim_requests": [{"id": t.id, "video_id": t.video_id, "trim_start": t.trim_start, "trim_end": t.trim_end} for t in trim_requests],
        "concat_requests": [{"id": c.id, "video_ids": [c.video_ids]} for c in concat_requests],
        "outputs": [{"id": f.id, "filename": f.filename} for f in outputs],
    })
