from flask import Flask, render_template, request, redirect, url_for, abort
import jwt
app = Flask(__name__)
JWT_SECRET = 'e2c10b4949aa6ca3913e2feab7964fc8'

def allow_without_auth(func):
    func._allow_without_auth = True
    return func

@app.before_request
def check_end_point():
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
    auth = request.headers.get('Authorization')
    try:
        assert auth is not None
        auth_components = auth.split(' ')
        assert len(auth_components) == 2
        token_type, token = auth_components
        assert token_type == 'Bearer'
        jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
    except Exception:
        return render_template('login.html')

@app.route('/', methods=['POST'])
def index():
    return render_template('index.html')

@app.route('/api/auth', methods=['POST'])
@allow_without_auth
def get_auth_header():
    user_obj = {'foo':'bar'}
    return jwt.encode(user_obj, JWT_SECRET, algorithm='HS256')
