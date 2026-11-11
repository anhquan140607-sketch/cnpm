import jwt
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from src.models import db

SECRET_KEY = "your-flask-secret-key"

def register_user(username, email, password):
    hashed_pw = generate_password_hash(password)
    sql = "INSERT INTO users (username, email, password_hash) VALUES (:u, :e, :p) RETURNING id"
    res = db.session.execute(db.text(sql), {"u": username, "e": email, "p": hashed_pw})
    db.session.commit()
    return res.fetchone()[0]

def login_user(email, password):
    sql = "SELECT id, password_hash FROM users WHERE email = :e"
    user = db.session.execute(db.text(sql), {"e": email}).fetchone()
    if user and check_password_hash(user.password_hash, password):
        payload = {
            "user_id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return token
    return None
