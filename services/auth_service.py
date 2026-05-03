from werkzeug.security import generate_password_hash, check_password_hash
from services.db_service import get_db


def create_user(full_name, business_name, email, password):
    db = get_db()
    password_hash = generate_password_hash(password)

    db.execute(
        """
        INSERT INTO users (full_name, business_name, email, password_hash)
        VALUES (?, ?, ?, ?)
        """,
        (full_name, business_name, email, password_hash)
    )

    db.commit()


def get_user_by_email(email):
    db = get_db()

    return db.execute(
        """
        SELECT * FROM users
        WHERE email = ?
        """,
        (email,)
    ).fetchone()


def get_user_by_id(user_id):
    db = get_db()

    return db.execute(
        """
        SELECT * FROM users
        WHERE id = ?
        """,
        (user_id,)
    ).fetchone()


def verify_user(email, password):
    user = get_user_by_email(email)

    if user and check_password_hash(user["password_hash"], password):
        return user

    return None