from db import DatabaseSession


def init_db():
    init_db_script = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        fullname VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS status (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        title VARCHAR(100) NOT NULL,
        description TEXT,
        status_id INTEGER REFERENCES status(id),
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
    );

    INSERT INTO status (name)
    VALUES ('new'), ('in progress'), ('completed')
    ON CONFLICT (name) DO NOTHING;
    """
    with DatabaseSession() as session:
        session.cursor.execute(init_db_script)
        print("Tables created and default statuses inserted")


if __name__ == "__main__":
    init_db()
