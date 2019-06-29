from flask import Flask, render_template, request, redirect, url_for, abort, g
import jwt
app = Flask(__name__)
JWT_SECRET = 'e2c10b4949aa6ca3913e2feab7964fc8'

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

@app.route('/', methods=['POST'])
@allow_for_roles(['admin'])
def index():
    return render_template('index.html')

@app.route('/api/auth', methods=['POST'])
@allow_without_auth
def get_auth_header():
    user_obj = {'name': 'John', 'role': 'admin'}
    return jwt.encode(user_obj, JWT_SECRET, algorithm='HS256')
