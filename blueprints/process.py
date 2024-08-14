from flask import current_app, jsonify
import os
import uuid
from models import db, TrimRequest, ConcatRequest, FinalVideo
from tasks import process_videos_async  # 수정된 함수 이름을 가져옵니다.
from . import process_bp

@process_bp.route('/process', methods=['POST'])
def process_videos():
    trim_requests = TrimRequest.query.all()
    concat_requests = ConcatRequest.query.all()

    final_video_id = str(uuid.uuid4())
    final_filename = f"{final_video_id}.mp4"
    final_filepath = os.path.join(current_app.config['FINAL_FOLDER'], final_filename)

    process_videos_async(trim_requests, concat_requests, current_app.config['UPLOAD_FOLDER'], final_filepath)

    final_video = FinalVideo(id=final_video_id, filename=final_filename)
    db.session.add(final_video)
    db.session.commit()

    # Clear processed requests
    db.session.query(TrimRequest).delete()
    db.session.query(ConcatRequest).delete()
    db.session.commit()

    return jsonify({"final_video_id": final_video_id, "download_url": f"/download/{final_video_id}"}), 200
