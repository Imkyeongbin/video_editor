from flask import Flask, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os
import uuid
from models import db, Video, TrimRequest, ConcatRequest, FinalVideo
from tasks import build_ffmpeg_commands, execute_ffmpeg_commands
from blueprints.views.index import index as index_page
from blueprints import upload_bp, trim_bp, concat_bp, process_bp, download_bp, status_bp

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
app.register_blueprint(index_page) # 인덱스 페이지
app.register_blueprint(upload_bp) # 동영상 업로드
app.register_blueprint(trim_bp) # 트림 요청
app.register_blueprint(concat_bp) # 이어 붙이기 요청
app.register_blueprint(process_bp) # 명령 작업 수행
app.register_blueprint(download_bp) # 최종 동영상 다운로드
app.register_blueprint(status_bp) # 동영상 및 작업 조회

if __name__ == '__main__':
    
    app.run(debug=True)
