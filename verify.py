from database import get_db
from werkzeug.security import generate_password_hash, check_password_hash

def create_user(username, password):
    conn = get_db()
    password_hash = generate_password_hash(password)

    try:
        conn.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash)
        )
        conn.commit()
        return "User created successfully"
    except:
        return "Username already exists"
    finally:
        conn.close()


def verify_user(username, password):
    conn = get_db()

    user = conn.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    ).fetchone()

    conn.close()
    if user and check_password_hash(user["password_hash"], password):
        return user
    
    return None

