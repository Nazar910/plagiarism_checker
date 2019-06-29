from flask import Flask, render_template, request, redirect, url_for, abort, g
import jwt
import os
from flask_pymongo import PyMongo
from src.services import UserService
app = Flask(__name__)
JWT_SECRET = os.getenv('JWT_SECRET')
assert JWT_SECRET
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
assert ADMIN_EMAIL
ADMIN_PASS = os.getenv('ADMIN_PASS')
assert ADMIN_PASS
app.config["MONGO_URI"] = os.getenv('MONGO_URI')
mongo = PyMongo(app)

@app.before_first_request
def ensure_admin():
    service = UserService(mongo.db.users)
    service.ensure_admin_user(ADMIN_EMAIL, ADMIN_PASS)

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
        return render_template('login.html')

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/api/auth', methods=['POST'])
@allow_without_auth
def get_auth_header():
    service = UserService(mongo.db.users)
    payload = request.get_json()
    email = payload['email']
    password = payload['password']
    user = service.find_by_email_and_password(email, password)
    user['_id'] = str(user['_id'])
    return jwt.encode(user, JWT_SECRET, algorithm='HS256')
