from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import uuid
from models import db, Video, TrimRequest, ConcatRequest, FinalVideo
from tasks import build_ffmpeg_commands, execute_ffmpeg_commands
from views.index import index as index_page

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['FINAL_FOLDER'] = 'outputs'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# 디렉토리 생성 함수
def create_directories():
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['FINAL_FOLDER'], exist_ok=True)

def _setup():
    db.create_all()
    create_directories()
    
app.before_request(_setup)

# 블루 프린트 등록
app.register_blueprint(index_page)

# 동영상 업로드
@app.route('/upload', methods=['POST'])
def upload_video():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file:
        filename = secure_filename(file.filename)
        video_id = str(uuid.uuid4())
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        video = Video(id=video_id, filename=filename)
        db.session.add(video)
        db.session.commit()

        return jsonify({"video_id": video_id}), 201

# 트림 요청
@app.route('/trim', methods=['POST'])
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

# 이어 붙이기 요청
@app.route('/concat', methods=['POST'])
def concat_videos():
    data = request.json
    video_ids = data.get('video_ids')

    if not video_ids or len(video_ids) < 2:
        return jsonify({"error": "At least two video IDs are required"}), 400

    concat_request = ConcatRequest(video_ids=','.join(video_ids))
    db.session.add(concat_request)
    db.session.commit()

    return jsonify({"message": "Concat request added"}), 201

# 명령 작업 수행
@app.route('/process', methods=['POST'])
def process_videos():
    trim_requests = TrimRequest.query.all()
    concat_requests = ConcatRequest.query.all()

    final_video_id = str(uuid.uuid4())
    final_filename = f"{final_video_id}.mp4"
    final_filepath = os.path.join(app.config['FINAL_FOLDER'], final_filename)

    commands = build_ffmpeg_commands(trim_requests, concat_requests, app.config['UPLOAD_FOLDER'], final_filepath)
    execute_ffmpeg_commands(commands)

    final_video = FinalVideo(id=final_video_id, filename=final_filename)
    db.session.add(final_video)
    db.session.commit()

    # Clear processed requests
    db.session.query(TrimRequest).delete()
    db.session.query(ConcatRequest).delete()
    db.session.commit()

    return jsonify({"final_video_id": final_video_id, "download_url": f"/download/{final_video_id}"}), 200

# 최종 동영상 다운로드
@app.route('/download/<video_id>', methods=['GET'])
def download_final_video(video_id):
    final_video = FinalVideo.query.filter_by(id=video_id).first()
    if not final_video:
        return jsonify({"error": "Final video not found"}), 404

    filepath = os.path.join(app.config['FINAL_FOLDER'], final_video.filename)
    return send_file(filepath, as_attachment=True)

# 동영상 및 작업 조회
@app.route('/videos', methods=['GET'])
def list_videos():
    videos = Video.query.all()
    trim_requests = TrimRequest.query.all()
    concat_requests = ConcatRequest.query.all()
    outputs = FinalVideo.query.all()

    return jsonify({
        "videos": [{"id": v.id, "filename": v.filename} for v in videos],
        "trim_requests": [{"id": t.id, "video_id": t.video_id, "trim_start": t.trim_start, "trim_end": t.trim_end} for t in trim_requests],
        "concat_requests": [{"id": c.id, "video_ids": c.video_ids} for c in concat_requests],
        "outputs": [{"id": f.id, "filename": f.filename} for f in outputs],
    })

if __name__ == '__main__':
    
    app.run(debug=True)
