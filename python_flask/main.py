from flask import Flask, jsonify, request, send_file, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect, text
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
import time
import requests
from datetime import datetime, timedelta
import json
import subprocess
from urllib.parse import quote
import tempfile
import io

# 初始化Flask应用
db = SQLAlchemy()

class User(db.Model):
    """用户模型"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def set_password(self, password):
        """设置密码哈希"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Note(db.Model):
    """笔记模型"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    emotion = db.Column(db.Integer)
    audio_path = db.Column(db.String(500))
    audio_data = db.Column(db.LargeBinary)
    audio_mime = db.Column(db.String(120))
    audio_filename = db.Column(db.String(255))
    audio_duration = db.Column(db.Integer)
    sentiment_score = db.Column(db.Float)
    analysis_result = db.Column(db.Text)
    analyzed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship('User', backref='notes')

# 创建Flask应用
# 关闭 Flask 默认 /static 路由，避免与前端 H5 静态资源路径冲突。
app = Flask(__name__, static_folder=None)

# 配置
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///warmlabel.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key-change-this')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=7)

UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads', 'audio')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
model_service_url = os.environ.get('MODEL_SERVICE_URL', 'http://127.0.0.1:8000/predict')
app.config['MODEL_SERVICE_URL'] = model_service_url
app.config['FFMPEG_PATH'] = os.environ.get('FFMPEG_PATH', 'ffmpeg')
app.config['MODEL_ANALYZE_URL'] = os.environ.get('MODEL_ANALYZE_URL', model_service_url)

LOCAL_RESOURCE_ROOT = os.path.join(app.root_path, 'local_resources')
LOCAL_EMOTION_FEED_FILE = os.path.join(LOCAL_RESOURCE_ROOT, 'emotion_feeds.json')
LOCAL_MUSIC_FILE = os.path.join(LOCAL_RESOURCE_ROOT, 'music_list.json')
WEB_DIST_ROOT = os.path.join(app.root_path, 'web_dist')
WEB_INDEX_FILE = os.path.join(WEB_DIST_ROOT, 'index.html')

os.makedirs(LOCAL_RESOURCE_ROOT, exist_ok=True)
os.makedirs(os.path.join(LOCAL_RESOURCE_ROOT, 'audio'), exist_ok=True)
os.makedirs(os.path.join(LOCAL_RESOURCE_ROOT, 'images'), exist_ok=True)


def serve_h5_index_or_backend_message():
    if os.path.exists(WEB_INDEX_FILE):
        return send_from_directory(WEB_DIST_ROOT, 'index.html')
    return jsonify({"message": "WarmLabel backend is running"})


def api_ok(data=None, message='ok'):
    return jsonify({'code': 0, 'message': message, 'data': data if data is not None else {}}), 200


def api_error(message, status=400, code=1, data=None):
    payload = {'code': code, 'message': message}
    if data is not None:
        payload['data'] = data
    return jsonify(payload), status


def parse_allowed_origins():
    raw_value = os.environ.get('CORS_ALLOWED_ORIGINS', '').strip()
    if not raw_value:
        return [
            'http://localhost:8080',
            'http://127.0.0.1:8080',
            'http://localhost:5173',
            'http://127.0.0.1:5173'
        ]
    return [item.strip() for item in raw_value.split(',') if item.strip()]

# 初始化扩展
db.init_app(app)
CORS(
    app,
    resources={r"/api/*": {"origins": parse_allowed_origins()}},
    supports_credentials=True
)
jwt = JWTManager(app)

# 创建数据库表
with app.app_context():
    db.create_all()

    def ensure_note_columns():
        dialect = db.engine.dialect.name
        if dialect not in ('sqlite', 'postgresql'):
            return

        inspector = inspect(db.engine)
        if 'note' not in inspector.get_table_names():
            return

        columns = {col['name'] for col in inspector.get_columns('note')}

        datetime_type = 'DATETIME' if dialect == 'sqlite' else 'TIMESTAMP'
        binary_type = 'BLOB' if dialect == 'sqlite' else 'BYTEA'

        pending = []
        if 'analysis_result' not in columns:
            pending.append("ALTER TABLE note ADD COLUMN analysis_result TEXT")
        if 'analyzed_at' not in columns:
            pending.append(f"ALTER TABLE note ADD COLUMN analyzed_at {datetime_type}")
        if 'audio_duration' not in columns:
            pending.append("ALTER TABLE note ADD COLUMN audio_duration INTEGER")
        if 'audio_data' not in columns:
            pending.append(f"ALTER TABLE note ADD COLUMN audio_data {binary_type}")
        if 'audio_mime' not in columns:
            pending.append("ALTER TABLE note ADD COLUMN audio_mime VARCHAR(120)")
        if 'audio_filename' not in columns:
            pending.append("ALTER TABLE note ADD COLUMN audio_filename VARCHAR(255)")

        for statement in pending:
            db.session.execute(text(statement))
        if pending:
            db.session.commit()

    ensure_note_columns()

@app.route("/")
def index():
    """首页"""
    return serve_h5_index_or_backend_message()

@app.route("/api/register", methods=["POST"])
def register():
    """用户注册接口"""
    try:
        data = request.get_json()
        
        # 验证必填字段
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if not username or not email or not password:
            return jsonify({'error': 'Username, email and password are required'}), 400
        
        # 验证用户名长度
        if len(username) < 3:
            return jsonify({'error': 'Username must be at least 3 characters long'}), 400
            
        # 验证邮箱格式
        if '@' not in email:
            return jsonify({'error': 'Invalid email format'}), 400
            
        # 验证密码长度
        if len(password) < 6:
            return jsonify({'error': 'Password must be at least 6 characters long'}), 400
        
        # 检查用户名是否已存在
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 409
            
        # 检查邮箱是否已存在
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already exists'}), 409
        
        # 创建新用户
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        # 创建JWT令牌
        access_token = create_access_token(identity=str(new_user.id))
        
        return jsonify({
            'message': 'User registered successfully',
            'user': new_user.to_dict(),
            'token': access_token
        }), 201
        
    except Exception as e:
        app.logger.exception('create_note failed')
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route("/api/login", methods=["POST"])
def login():
    """用户登录接口"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
            
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password are required'}), 400
        
        # 查找用户
        user = User.query.filter_by(username=username).first()
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        # 验证密码
        if not user.check_password(password):
            return jsonify({'error': 'Invalid password'}), 401
        
        # 创建JWT令牌
        access_token = create_access_token(identity=str(user.id))
        
        return jsonify({
            'message': 'Login successful',
            'user': user.to_dict(),
            'token': access_token
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/api/profile", methods=["GET"])
@jwt_required()
def get_profile():
    """获取用户个人信息"""
    try:
        user_id = get_jwt_identity()
        user = User.query.get(int(user_id))
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        return jsonify({'user': user.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route("/api/health", methods=["GET"])
def health_check():
    """健康检查接口"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat() + 'Z'}), 200


@app.route('/api/model-status', methods=['GET'])
def model_status():
    """模型服务状态接口"""
    model_url = (app.config.get('MODEL_ANALYZE_URL') or '').strip()
    if is_placeholder_model_url(model_url):
        return jsonify({
            'configured': False,
            'reachable': False,
            'message': 'MODEL_ANALYZE_URL 未配置'
        }), 200

    reachable = False
    status_code = None
    message = '模型服务不可达'

    try:
        # 模型服务通常是 POST 接口，这里使用 GET 仅用于连通性探测。
        resp = requests.get(model_url, timeout=3)
        status_code = resp.status_code
        if 200 <= resp.status_code < 500:
            reachable = True
            message = '模型服务可达'
    except requests.RequestException as exc:
        message = str(exc)

    return jsonify({
        'configured': True,
        'reachable': reachable,
        'status_code': status_code,
        'message': message
    }), 200


def ensure_wav_for_model(audio_path):
    if not audio_path:
        return None

    ext = os.path.splitext(audio_path)[1].lower()
    if ext == '.wav':
        return audio_path

    wav_path = f"{os.path.splitext(audio_path)[0]}_16k.wav"
    if os.path.exists(wav_path):
        return wav_path

    try:
        subprocess.run(
            [
                app.config['FFMPEG_PATH'],
                '-y',
                '-i',
                audio_path,
                '-ac',
                '1',
                '-ar',
                '16000',
                wav_path
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return wav_path
    except (OSError, subprocess.CalledProcessError):
        return audio_path


def parse_int_or_none(value):
    if value in (None, ''):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def format_datetime_z(value):
    if not value:
        return None
    return value.isoformat() + 'Z'


def create_temp_audio_file(audio_bytes, filename_hint='audio.wav'):
    if not audio_bytes:
        return None
    ext = os.path.splitext(filename_hint or '')[1].lower() or '.wav'
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        tmp.write(audio_bytes)
        return tmp.name


def resolve_note_audio_for_model(note):
    if note.audio_data:
        filename = note.audio_filename or 'audio.wav'
        temp_path = create_temp_audio_file(note.audio_data, filename)
        return temp_path, True
    if note.audio_path and os.path.exists(note.audio_path):
        return note.audio_path, False
    return None, False


def cleanup_temp_audio_files(*paths):
    for path in paths:
        if not path:
            continue
        try:
            if os.path.exists(path):
                os.remove(path)
        except OSError:
            pass


def note_audio_url(note):
    has_audio = bool(note.audio_data) or bool(note.audio_path)
    if not has_audio:
        return None
    return f"{request.host_url.rstrip('/')}/api/notes/{note.id}/audio"


def load_json_array(file_path, default_items):
    if not os.path.exists(file_path):
        return default_items
    try:
        # Support UTF-8 with BOM (common when files are saved via Windows PowerShell).
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            payload = json.load(f)
        if isinstance(payload, list):
            return payload
    except (OSError, json.JSONDecodeError):
        pass
    return default_items


def local_resource_url(path_value):
    if not path_value:
        return None
    text = str(path_value).strip()
    if not text:
        return None
    if text.startswith('http://') or text.startswith('https://'):
        return text
    normalized = text.lstrip('/').replace('\\', '/')
    encoded = '/'.join(quote(part) for part in normalized.split('/'))
    return f"{request.host_url.rstrip('/')}/api/local-resources/{encoded}"


def normalize_emotion_tag(raw_value):
    text = str(raw_value or '').strip().lower()
    map_table = {
        '1': '1',
        '2': '2',
        '3': '3',
        '低落预警': '1',
        '低落': '1',
        'sad': '1',
        '平稳': '2',
        'stable': '2',
        '高兴': '3',
        '开心': '3',
        'happy': '3'
    }
    return map_table.get(text, '')


RESOURCE_GROUP_META = {
    '1': {
        'key': 'relief',
        'name': '舒缓减压',
        'audience': '低落预警人群',
        'description': '优先推送安抚型图文、呼吸放松与情绪承接内容。'
    },
    '2': {
        'key': 'balance',
        'name': '稳定维持',
        'audience': '平稳人群',
        'description': '优先推送习惯维护、轻复盘与节奏管理内容。'
    },
    '3': {
        'key': 'thrive',
        'name': '激活成长',
        'audience': '积极高兴人群',
        'description': '优先推送目标推进、行动放大与成长型内容。'
    }
}


def resource_group_info(tag):
    return RESOURCE_GROUP_META.get(tag or '', {
        'key': 'general',
        'name': '通用资源',
        'audience': '全部人群',
        'description': '适用于全部用户的通用内容。'
    })


def load_emotion_feed_rows(target_tag=''):
    default_items = [
        {
            'emotion_tag': '1',
            'type': 'imageText',
            'title': '低落期自我支持清单',
            'desc': '先稳住，再行动，先从最小步开始。',
            'detail': '先做一件5分钟内可完成的小事，再决定下一步。',
            'is_active': True
        },
        {
            'emotion_tag': '2',
            'type': 'imageText',
            'title': '稳定情绪维护法',
            'desc': '固定作息和轻量复盘，保持心态稳定。',
            'detail': '每天固定10分钟复盘，记录最稳的一刻。',
            'is_active': True
        },
        {
            'emotion_tag': '3',
            'type': 'video',
            'title': '积极状态放大术',
            'desc': '趁状态好，把可执行目标拆小并推进。',
            'url': 'https://www.bilibili.com/video/BV1V4411Z7VA',
            'is_active': True
        }
    ]
    source = load_json_array(LOCAL_EMOTION_FEED_FILE, default_items)
    image_text = []
    videos = []

    for item in source:
        if not isinstance(item, dict):
            continue
        if item.get('is_active', True) is False:
            continue

        tag = normalize_emotion_tag(item.get('emotion_tag'))
        if target_tag and tag and tag != target_tag:
            continue

        row = {
            'title': item.get('title') or '未命名内容',
            'desc': item.get('desc') or '',
            'detail': item.get('detail') or item.get('desc') or '',
            'emotion_tag': tag
        }
        group_info = resource_group_info(tag)
        row['group_key'] = group_info['key']
        row['group_name'] = group_info['name']

        item_type = str(item.get('type') or 'imageText').strip()
        if item_type == 'video':
            row['url'] = local_resource_url(item.get('url'))
            row['cover'] = local_resource_url(item.get('cover'))
            if row['url']:
                videos.append(row)
        else:
            row['cover'] = local_resource_url(item.get('cover'))
            image_text.append(row)

    return image_text, videos


def load_music_rows(target_tag=''):
    default_items = [
        {
            'emotion_tag': '2',
            'name': 'Calm Demo',
            'author': 'WarmLabel',
            'url': 'audio/calm_demo.mp3',
            'is_active': True
        }
    ]
    source = load_json_array(LOCAL_MUSIC_FILE, default_items)
    music_items = []

    for item in source:
        if not isinstance(item, dict):
            continue
        if item.get('is_active', True) is False:
            continue

        tag = normalize_emotion_tag(item.get('emotion_tag'))
        if target_tag and tag and tag != target_tag:
            continue

        group_info = resource_group_info(tag)
        row = {
            'name': item.get('name') or '未命名音乐',
            'author': item.get('author') or '未知创作者',
            'url': local_resource_url(item.get('url')),
            'cover': local_resource_url(item.get('cover')),
            'duration': item.get('duration'),
            'emotion_tag': tag,
            'group_key': group_info['key'],
            'group_name': group_info['name']
        }
        if row['url']:
            music_items.append(row)

    return music_items


def is_placeholder_model_url(url):
    text = (url or '').strip().lower()
    return (not text) or ('your-model-service.example.com' in text)


def build_local_fallback_analysis(text):
    content = str(text or '').strip().lower()
    if not content:
        probs = [0.2, 0.6, 0.2]
        pred = 2
    else:
        negative_words = ['难过', '痛苦', '焦虑', '崩溃', 'sad', 'depress', 'tired', '烦', '累']
        positive_words = ['开心', '高兴', '满足', '放松', 'happy', 'great', 'good', '轻松', '顺利']
        neg_score = sum(1 for w in negative_words if w in content)
        pos_score = sum(1 for w in positive_words if w in content)

        if neg_score > pos_score:
            probs = [0.72, 0.20, 0.08]
            pred = 1
        elif pos_score > neg_score:
            probs = [0.10, 0.22, 0.68]
            pred = 3
        else:
            probs = [0.16, 0.68, 0.16]
            pred = 2

    return {
        'prediction': pred,
        'probabilities': {
            'M': probs,
            'T': probs,
            'A': probs
        },
        'source': 'local-fallback'
    }


@app.route('/api/local-resources/<path:resource_path>', methods=['GET'])
def get_local_resource(resource_path):
    abs_root = os.path.abspath(LOCAL_RESOURCE_ROOT)
    abs_target = os.path.abspath(os.path.join(LOCAL_RESOURCE_ROOT, resource_path))

    if os.path.commonpath([abs_root, abs_target]) != abs_root:
        return jsonify({'error': '非法资源路径'}), 400
    if not os.path.exists(abs_target):
        return jsonify({'error': '资源不存在'}), 404

    return send_from_directory(LOCAL_RESOURCE_ROOT, resource_path, as_attachment=False)


@app.route('/api/emotion-feeds', methods=['GET'])
def get_emotion_feeds():
    target_tag = normalize_emotion_tag(request.args.get('emotion'))
    image_text, videos = load_emotion_feed_rows(target_tag)

    return jsonify({
        'emotion_tag': target_tag,
        'imageText': image_text,
        'videos': videos
    }), 200


@app.route('/api/music-recommendations', methods=['GET'])
def get_music_recommendations():
    target_tag = normalize_emotion_tag(request.args.get('emotion'))
    music_items = load_music_rows(target_tag)

    return jsonify({'items': music_items}), 200


@app.route('/api/resource-bundles', methods=['GET'])
def get_resource_bundles():
    target_tag = normalize_emotion_tag(request.args.get('emotion'))
    image_text, videos = load_emotion_feed_rows('')
    musics = load_music_rows('')

    groups = {}
    for tag in ('1', '2', '3'):
        meta = resource_group_info(tag)
        groups[tag] = {
            'emotion_tag': tag,
            'group_key': meta['key'],
            'group_name': meta['name'],
            'audience': meta['audience'],
            'description': meta['description'],
            'imageText': [],
            'videos': [],
            'music': []
        }

    for item in image_text:
        tag = normalize_emotion_tag(item.get('emotion_tag'))
        if tag in groups:
            groups[tag]['imageText'].append(item)

    for item in videos:
        tag = normalize_emotion_tag(item.get('emotion_tag'))
        if tag in groups:
            groups[tag]['videos'].append(item)

    for item in musics:
        tag = normalize_emotion_tag(item.get('emotion_tag'))
        if tag in groups:
            groups[tag]['music'].append(item)

    recommended_tag = target_tag if target_tag in groups else ''
    if not recommended_tag:
        max_tag = ''
        max_total = -1
        for tag, block in groups.items():
            total = len(block['imageText']) + len(block['videos']) + len(block['music'])
            if total > max_total:
                max_total = total
                max_tag = tag
        recommended_tag = max_tag

    return api_ok({
        'recommended_emotion_tag': recommended_tag,
        'recommended_group': groups.get(recommended_tag),
        'groups': groups
    }, message='资源分群加载成功')


@app.route('/api/notes', methods=['POST'])
@jwt_required()
def create_note():
    """创建笔记并调用模型服务"""
    try:
        user_id = int(get_jwt_identity())

        payload = request.form if request.form else (request.get_json(silent=True) or {})
        title = payload.get('title')
        content = payload.get('content')
        emotion = payload.get('emotion')
        audio_duration_raw = payload.get('audio_duration')
        emotion_value = int(emotion) if emotion is not None else None
        audio_duration = parse_int_or_none(audio_duration_raw)

        if not title or not content or emotion_value is None:
            return jsonify({'error': 'Title, content and emotion are required'}), 400

        audio_file = request.files.get('audio')
        audio_path = None
        audio_bytes = None
        audio_filename = None
        audio_mime = None
        temp_audio_path = None
        if audio_file:
            original_name = secure_filename(audio_file.filename or '')
            ext = os.path.splitext(original_name)[1].lower() or '.wav'
            audio_filename = f"{user_id}_{int(time.time())}{ext}"
            audio_bytes = audio_file.read()
            if audio_bytes:
                audio_mime = (audio_file.mimetype or 'application/octet-stream')[:120]
                temp_audio_path = create_temp_audio_file(audio_bytes, audio_filename)
                audio_path = audio_filename

        sentiment_score = None
        if content and temp_audio_path:
            model_audio_path = ensure_wav_for_model(temp_audio_path)
            try:
                with open(model_audio_path, 'rb') as audio_stream:
                    files = {'audio': audio_stream}
                    data = {'text': content}
                    response = requests.post(app.config['MODEL_SERVICE_URL'], data=data, files=files, timeout=10)
                if response.status_code == 200:
                    sentiment_score = response.json().get('prediction')
            except requests.RequestException:
                sentiment_score = None
            finally:
                cleanup_temp_audio_files(model_audio_path if model_audio_path != temp_audio_path else None, temp_audio_path)

        note = Note(
            user_id=user_id,
            title=title,
            content=content,
            emotion=emotion_value,
            audio_path=audio_path,
            audio_data=audio_bytes,
            audio_mime=audio_mime,
            audio_filename=audio_filename,
            audio_duration=audio_duration,
            sentiment_score=sentiment_score
        )
        db.session.add(note)
        db.session.commit()

        return jsonify({
            'message': '笔记保存成功',
            'note_id': note.id,
            'sentiment': sentiment_score
        }), 201
    except Exception as e:
        app.logger.exception('update_note failed')
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/notes', methods=['GET'])
@jwt_required()
def get_notes():
    """获取当前用户的笔记列表"""
    user_id = int(get_jwt_identity())
    notes = Note.query.filter_by(user_id=user_id).order_by(Note.created_at.desc()).all()
    return jsonify([
        {
            'id': note.id,
            'title': note.title,
            'content': (note.content[:50] + '...') if note.content and len(note.content) > 50 else note.content,
            'emotion': note.emotion,
            'audio_duration': note.audio_duration,
            'sentiment_score': note.sentiment_score,
            'analysis_result': note.analysis_result,
            'analyzed_at': format_datetime_z(note.analyzed_at),
            'created_at': format_datetime_z(note.created_at)
        }
        for note in notes
    ]), 200


@app.route('/api/notes/<int:note_id>', methods=['GET'])
@jwt_required()
def get_note(note_id):
    """获取笔记详情"""
    note = Note.query.get_or_404(note_id)
    if note.user_id != int(get_jwt_identity()):
        return jsonify({'error': '无权访问'}), 403

    return jsonify({
        'id': note.id,
        'title': note.title,
        'content': note.content,
        'emotion': note.emotion,
        'audio_path': note_audio_url(note),
        'audio_duration': note.audio_duration,
        'sentiment_score': note.sentiment_score,
        'analysis_result': note.analysis_result,
        'analyzed_at': format_datetime_z(note.analyzed_at),
        'created_at': format_datetime_z(note.created_at)
    }), 200


@app.route('/api/notes/<int:note_id>/analyze', methods=['POST'])
@jwt_required()
def analyze_note(note_id):
    """分析笔记内容和录音"""
    try:
        note = Note.query.get_or_404(note_id)
        if note.user_id != int(get_jwt_identity()):
            return jsonify({'error': '无权访问'}), 403

        model_url = (app.config.get('MODEL_ANALYZE_URL') or '').strip()
        if is_placeholder_model_url(model_url):
            result = build_local_fallback_analysis(note.content)
            note.analysis_result = json.dumps(result)
            note.analyzed_at = datetime.utcnow()
            db.session.commit()
            return jsonify({
                'message': '分析完成（兜底模式）',
                'note_id': note.id,
                'analysis': result,
                'analyzed_at': note.analyzed_at.isoformat() + 'Z'
            }), 200

        if not note.content or (not note.audio_data and not note.audio_path):
            return jsonify({'error': '需要文本与录音才能分析'}), 400

        original_audio_path, should_cleanup = resolve_note_audio_for_model(note)
        if not original_audio_path:
            return jsonify({'error': '录音不存在'}), 404

        model_audio_path = ensure_wav_for_model(original_audio_path)
        try:
            with open(model_audio_path, 'rb') as audio_stream:
                files = {'audio': audio_stream}
                data = {'text': note.content}
                response = requests.post(model_url, data=data, files=files, timeout=20)
        finally:
            cleanup_temp_audio_files(
                model_audio_path if model_audio_path != original_audio_path else None,
                original_audio_path if should_cleanup else None
            )

        if response.status_code != 200:
            detail = None
            try:
                detail = response.json()
            except ValueError:
                detail = response.text
            return jsonify({'error': '模型服务调用失败', 'model_status': response.status_code, 'detail': detail}), 502

        try:
            result = response.json()
        except ValueError:
            result = {'raw': response.text}

        note.analysis_result = json.dumps(result)
        note.analyzed_at = datetime.utcnow()
        db.session.commit()

        return jsonify({
            'message': '分析完成',
            'note_id': note.id,
            'analysis': result,
            'analyzed_at': note.analyzed_at.isoformat() + 'Z'
        }), 200
    except requests.RequestException as e:
        app.logger.exception('analyze_note model request failed')
        if 'note' in locals() and note:
            result = build_local_fallback_analysis(note.content)
            note.analysis_result = json.dumps(result)
            note.analyzed_at = datetime.utcnow()
            db.session.commit()
            return jsonify({
                'message': '分析完成（兜底模式）',
                'note_id': note.id,
                'analysis': result,
                'analyzed_at': note.analyzed_at.isoformat() + 'Z',
                'fallback_reason': str(e)
            }), 200
        return jsonify({'error': str(e)}), 500
    except Exception as e:
        app.logger.exception('analyze_note failed')
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/notes/<int:note_id>/audio', methods=['GET'])
@jwt_required()
def get_note_audio(note_id):
    """获取笔记录音文件"""
    note = Note.query.get_or_404(note_id)
    if note.user_id != int(get_jwt_identity()):
        return jsonify({'error': '无权访问'}), 403

    if note.audio_data:
        return send_file(
            io.BytesIO(note.audio_data),
            mimetype=note.audio_mime or 'application/octet-stream',
            as_attachment=False,
            download_name=note.audio_filename or f'note_{note.id}.wav'
        )

    if not note.audio_path or not os.path.exists(note.audio_path):
        return jsonify({'error': '录音不存在'}), 404

    return send_file(note.audio_path, as_attachment=False)


@app.route('/api/notes/<int:note_id>', methods=['PUT', 'POST'])
@jwt_required()
def update_note(note_id):
    """更新笔记"""
    try:
        note = Note.query.get_or_404(note_id)
        if note.user_id != int(get_jwt_identity()):
            return jsonify({'error': '无权访问'}), 403

        payload = request.form if request.form else (request.get_json(silent=True) or {})
        title = payload.get('title')
        content = payload.get('content')
        emotion = payload.get('emotion')
        audio_duration_raw = payload.get('audio_duration')
        emotion_value = int(emotion) if emotion is not None else None
        audio_duration = parse_int_or_none(audio_duration_raw)

        if not title or not content or emotion_value is None:
            return jsonify({'error': 'Title, content and emotion are required'}), 400

        audio_file = request.files.get('audio')
        if audio_file:
            original_name = secure_filename(audio_file.filename or '')
            ext = os.path.splitext(original_name)[1].lower() or '.wav'
            filename = f"{note.user_id}_{int(time.time())}{ext}"
            uploaded_bytes = audio_file.read()

            if note.audio_path and os.path.exists(note.audio_path):
                try:
                    os.remove(note.audio_path)
                except OSError:
                    pass

            note.audio_path = filename if uploaded_bytes else note.audio_path
            note.audio_data = uploaded_bytes if uploaded_bytes else note.audio_data
            note.audio_mime = (audio_file.mimetype or 'application/octet-stream')[:120] if uploaded_bytes else note.audio_mime
            note.audio_filename = filename if uploaded_bytes else note.audio_filename

        sentiment_score = note.sentiment_score
        if content and (note.audio_data or note.audio_path):
            source_audio_path, should_cleanup = resolve_note_audio_for_model(note)
            if source_audio_path:
                model_audio_path = ensure_wav_for_model(source_audio_path)
            else:
                model_audio_path = None
            try:
                if model_audio_path:
                    with open(model_audio_path, 'rb') as audio_stream:
                        files = {'audio': audio_stream}
                        data = {'text': content}
                        response = requests.post(app.config['MODEL_SERVICE_URL'], data=data, files=files, timeout=10)
                    if response.status_code == 200:
                        sentiment_score = response.json().get('prediction')
            except requests.RequestException:
                sentiment_score = note.sentiment_score
            finally:
                cleanup_temp_audio_files(
                    model_audio_path if model_audio_path and model_audio_path != source_audio_path else None,
                    source_audio_path if 'should_cleanup' in locals() and should_cleanup else None
                )

        note.title = title
        note.content = content
        note.emotion = emotion_value
        if audio_duration is not None:
            note.audio_duration = audio_duration
        note.sentiment_score = sentiment_score

        db.session.commit()

        return jsonify({
            'message': '笔记更新成功',
            'note_id': note.id,
            'sentiment': sentiment_score
        }), 200
    except Exception as e:
        app.logger.exception('analyze_note failed')
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/notes/<int:note_id>', methods=['DELETE'])
@jwt_required()
def delete_note(note_id):
    """删除笔记"""
    try:
        note = Note.query.get_or_404(note_id)
        if note.user_id != int(get_jwt_identity()):
            return jsonify({'error': '无权访问'}), 403

        if note.audio_path and os.path.exists(note.audio_path):
            try:
                os.remove(note.audio_path)
            except OSError:
                pass

        db.session.delete(note)
        db.session.commit()
        return jsonify({'message': '笔记删除成功'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/<path:path>', methods=['GET'])
def serve_h5_assets(path):
    if path.startswith('api/'):
        return jsonify({'error': 'Not found'}), 404

    target = os.path.join(WEB_DIST_ROOT, path)
    if os.path.isfile(target):
        return send_from_directory(WEB_DIST_ROOT, path)

    return serve_h5_index_or_backend_message()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
    