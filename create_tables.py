from connection import get_postgres_conn

def create_tables():
    conn = get_postgres_conn()
    cur  = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id    VARCHAR(50)  PRIMARY KEY,
            name  VARCHAR(100),
            email VARCHAR(150) UNIQUE,
            age   INTEGER
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS address (
            id                SERIAL       PRIMARY KEY,
            user_id           VARCHAR(50)  REFERENCES users(id),
            street            VARCHAR(200),
            city              VARCHAR(100),
            country           VARCHAR(100),
            activity_location VARCHAR(100)
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS activity (
            id         VARCHAR(50)  PRIMARY KEY,
            user_id    VARCHAR(50)  REFERENCES users(id),
            action     TEXT,
            timestamp  TIMESTAMPTZ,
            ip_address VARCHAR(50)
        );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("PostgreSQL tables created (users, address, activity)")

if __name__ == "__main__":
    create_tables()
