from flask import Blueprint

upload_bp = Blueprint('upload', __name__)
trim_bp = Blueprint('trim', __name__)
concat_bp = Blueprint('concat', __name__)
process_bp = Blueprint('process', __name__)
download_bp = Blueprint('download', __name__)
status_bp = Blueprint('status', __name__)

# 여기서 블루프린트를 초기화하고 각 모듈에서 라우트를 임포트합니다.
from .upload import *
from .trim import *
from .concat import *
from .process import *
from .download import *
from .status import *
