from flask import Flask, request, jsonify, make_response, render_template, session, flash, redirect, url_for
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SasaankJaiminAyushMokshitAnirudh97SudoShankhesh'
CORS(app)

# Temporary data storage for registered users (in-memory dictionary)
users = {}

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        if not token:
            return jsonify({'Alert!': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'Message': 'Token has expired'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'Message': 'Invalid token'}), 403

        return func(*args, **kwargs)
    return decorated


@app.route('/')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login_page'))
    else:
        return 'You are currently logged in!'


@app.route('/public')
def public():
    return 'For Public'


@app.route('/auth')
@token_required
def auth():
    return 'JWT is verified. Welcome to your dashboard!'


@app.route('/login', methods=['POST'])
def login_page():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        # Validate username and password
        if username in users and users[username] == password:
            session['logged_in'] = True
            session['username'] = username  # Store username in session

            # Generate JWT token
            token = jwt.encode({
                'user': username,
                'exp': datetime.utcnow() + timedelta(seconds=60)
            }, app.config['SECRET_KEY'], algorithm="HS256")

            return jsonify({'token': token, 'message': 'Login successful!'}), 200
        else:
            return jsonify({'message': 'Invalid username or password!'}), 401



@app.route('/SignUp', methods=['POST','GET'])
def signup():
    data = request.get_json()  # Parse JSON data from the request
    username = data.get('username')
    password = data.get('password')
    
    # Ensure username and password are provided
    if not username or not password:
        return jsonify({'message': 'Username and password are required!'}), 400
    
    # Ensure username is unique
    if username in users:
        return jsonify({'message': 'Username already exists! Please choose a different one.'}), 409
    
    # Register the user
    users[username] = password
    return jsonify({'message': 'Signup successful! Please log in.'}), 201



@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
