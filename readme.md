# Video Editor API

## 설치 및 실행

1. 프로젝트 클론
    ```bash
    git clone https://github.com/yourrepo/video_editor.git
    cd video_editor
    ```

2. 가상 환경 생성 및 활성화
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # Windows에서는 .venv\Scripts\activate
    ```

3. 필요한 패키지 설치
    ```bash
    pip install -r requirements.txt
    ```

4. Flask 애플리케이션 실행
    ```bash
    flask run
    ```

## API 엔드포인트

### 1. 동영상 업로드

**POST** `/upload`

- **파일**: `multipart/form-data`, 키명 = file (필수, 여러 파일 가능)
- **응답**: 
    - 성공: `{"video_id": "<video_id>"}`
    - 실패: `{"error": "No file part"}`

### 2. 트림 요청

**POST** `/trim`

- **매개변수**: 
    - `video_id` (필수)
    - `trim_start` (밀리초, 필수)
    - `trim_end` (밀리초, 필수)

### 3. 이어 붙이기 요청

**POST** `/concat`

- **매개변수**: 
    - `video_ids` (ID 목록(리스트 형태-[]), 필수)

### 4. 명령 작업 수행

**POST** `/process`

- **응답**: 
    - 성공: `{"final_video_id": "<final_video_id>", "download_url": "/download/<final_video_id>"}`

### 5. 최종 동영상 다운로드

**GET** `/download/<video_id>`

### 6. 동영상 및 작업 조회

**GET** `/videos`

## 핵심 문제 해결 전략

1. **동시성 문제**: Flask는 기본적으로 단일 스레드에서 실행되기 때문에, 여러 동영상 업로드 및 처리 요청을 동시에 처리할 수 있습니다. 다만, 더 높은 동시성을 요구한다면 Gunicorn과 같은 WSGI 서버를 고려할 수 있습니다. ffmpeg 내장옵션인 threads를 활용하여 1코어이외에 전부 동시 작업하도록 하였습니다. 비동기 작업 처리를 위해 asyncio를 도입하여, 동영상 처리와 같은 시간이 오래 걸리는 작업을 비동기적으로 처리할 수 있습니다.
동시 작업량이 늘어나 스케일 아웃이 필요한 상황이 되면 celery와 redis를 활용하여 백그라운드 작업큐를 관리할 수 있을 것입니다.

2. **대용량 동영상 처리**: ffmpeg은 시스템 자원을 많이 사용하는 도구입니다. 이를 감안하여 ffmpeg 명령을 순차적으로 실행하며, 프로세스가 병목이 되지 않도록 주의합니다.

3. **확장성**: SQLite 대신 더 큰 규모의 데이터베이스(예: PostgreSQL)를 사용하거나, 클라우드 스토리지를 사용해 동영상 파일을 관리할 수 있습니다.

4. **속도 개선**: 데이터베이스로 인메모리 데이터 구조 저장소인 Redis와 같은 것을 사용하고 네트워크 속도가 느린 경우 데이터를 압축하여 전송합니다.
