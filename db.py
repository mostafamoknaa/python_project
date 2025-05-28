import psycopg2

def connect_db():
    return psycopg2.connect(
        dbname="project",
        user="mostafa",
        password="12345",
        host="localhost",
        port="5432"
    )

def create_tables():
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(50) NOT NULL
            );
            """)
            cur.execute("""
            CREATE TABLE IF NOT EXISTS loans (
                id SERIAL PRIMARY KEY,
                user_id INT REFERENCES users(id),
                amount NUMERIC,
                balance NUMERIC,
                payments TEXT DEFAULT ''
            );
            """)
        conn.commit()
