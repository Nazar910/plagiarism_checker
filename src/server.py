import os
from flask import Flask, render_template, request, abort, g, jsonify, send_from_directory
import jwt
from flask_pymongo import PyMongo
from googlesearch import search
from src.services import UserService, TextService
app = Flask(__name__, static_folder='static')
JWT_SECRET = os.getenv('JWT_SECRET')
assert JWT_SECRET
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
assert ADMIN_EMAIL
ADMIN_PASS = os.getenv('ADMIN_PASS')
assert ADMIN_PASS
app.config["MONGO_URI"] = os.getenv('MONGO_URI')
mongo = PyMongo(app)
# TODO: may be some issues in multiple threads
user_service = UserService(mongo.db.users)
text_service = TextService(mongo.db.texts)

@app.before_first_request
def ensure_admin():
    user_service.ensure_admin_user(ADMIN_EMAIL, ADMIN_PASS)

def allow_without_auth(func):
    func._allow_without_auth = True
    return func

def allow_for_roles(roles):
    def _allow_for_roles(func):
        def __allow_for_roles(*args, **kwargs):
            if g.decoded is None or g.decoded['role'] not in roles:
                abort(403)
            return func(*args, **kwargs)
        return __allow_for_roles
    return _allow_for_roles

@app.before_request
def check_endpoint():
    if request.endpoint not in app.view_functions:
        abort(404)

@app.before_request
def check_auth():
    do_auth = not hasattr(
        app.view_functions[request.endpoint],
        '_allow_without_auth'
    )
    if not do_auth:
        return
    try:
        auth = request.headers.get('Authorization')
        assert auth is not None
        auth_components = auth.split(' ')
        assert len(auth_components) == 2
        token_type, token = auth_components
        assert token_type == 'Bearer'
        result = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        g.decoded = result
    except Exception:
        abort(401)

@app.route('/', methods=['GET'])
@allow_without_auth
def index():
    return render_template('index.html')

@app.route('/api/profile', methods=['GET'])
def get_profile():
    user = g.decoded
    if user is None:
        abort(401)
    return jsonify({'user': user})

@app.route('/js-bundle')
@allow_without_auth
def send_js():
    return send_from_directory(app.static_folder, 'frontend/dist/index-bundle.js')

@app.route('/api/auth', methods=['POST'])
@allow_without_auth
def get_auth_header():
    payload = request.get_json()
    email = payload['email']
    password = payload['password']
    user = user_service.find_by_email_and_password(email, password)
    if user is None:
        abort(401)
    user['_id'] = str(user['_id'])
    token = jwt.encode(user, JWT_SECRET, algorithm='HS256')
    return jsonify({'token': token.decode('utf-8')})

@app.route('/api/check-for-plagiarism', methods=['POST'])
def check_for_plagiarism():
    payload = request.get_json()
    return jsonify(text_service.check_text_for_plagiarism(payload['text']))
