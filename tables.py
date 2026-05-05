from database import get_db

def create_tables():
    conn = get_db()

    conn.cursor().execute("""
    CREATE TABLE IF NOT EXISTS users (
        id serial PRIMARY KEY,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()