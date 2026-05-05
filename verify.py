from database import get_db
from werkzeug.security import generate_password_hash, check_password_hash

def create_user(username, password):
    conn = get_db()
    password_hash = generate_password_hash(password)

    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (username, password_hash),
        )
        conn.commit()
        return "User created successfully"
    except Exception as error:
        conn.rollback()
        return f"user already exists or error occurred: {error}"
    finally:
        conn.close()


def verify_user(username, password):
    conn = get_db()

    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username, password_hash FROM users WHERE username = %s",
            (username,),
        )
        user = cursor.fetchone()

        if user and check_password_hash(user[2], password):
            return user

        return None
    finally:
        conn.close()

