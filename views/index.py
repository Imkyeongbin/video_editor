from flask import Blueprint, render_template_string
index = Blueprint('index', __name__)

@index.route('/')
def main_page():
    html_content = """
    <h2>API 엔드포인트</h2>

    <h3>1. 동영상 업로드</h3>
    <p><strong>POST</strong> <code>/upload</code></p>
    <ul>
        <li><strong>파일</strong>: <code>`multipart/form-data`, 키명 = file (필수)</code></li>
        <li><strong>응답</strong>:</li>
        <ul>
            <li>성공: <code>{"video_id": "&lt;video_id&gt;"}</code></li>
            <li>실패: <code>{"error": "No file part"}</code></li>
        </ul>
    </ul>

    <h3>2. 트림 요청</h3>
    <p><strong>POST</strong> <code>/trim</code></p>
    <ul>
        <li><strong>매개변수</strong>:</li>
        <ul>
            <li><code>video_id</code> (필수)</li>
            <li><code>trim_start</code> (밀리초, 필수)</li>
            <li><code>trim_end</code> (밀리초, 필수)</li>
        </ul>
    </ul>

    <h3>3. 이어 붙이기 요청</h3>
    <p><strong>POST</strong> <code>/concat</code></p>
    <ul>
        <li><strong>매개변수</strong>: <code>video_ids</code> (ID 목록(리스트 형태-[]), 필수)</li>
    </ul>

    <h3>4. 명령 작업 수행</h3>
    <p><strong>POST</strong> <code>/process</code></p>
    <ul>
        <li><strong>응답</strong>:</li>
        <ul>
            <li>성공: <code>{"final_video_id": "&lt;final_video_id&gt;", "download_url": "/download/&lt;final_video_id&gt;"}</code></li>
        </ul>
    </ul>

    <h3>5. 최종 동영상 다운로드</h3>
    <p><strong>GET</strong> <code>/download/&lt;video_id&gt;</code></p>

    <h3>6. 동영상 및 작업 조회</h3>
    <p><strong>GET</strong> <code>/videos</code></p>
    """
    return render_template_string(html_content)