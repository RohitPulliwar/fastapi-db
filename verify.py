from werkzeug.security import check_password_hash, generate_password_hash

from tables import DBUser


def create_user(db, username, password, enrollment_number=None):
    try:
        existing_user = db.query(DBUser).filter(DBUser.username == username).first()

        if enrollment_number:
            existing_user = existing_user or db.query(DBUser).filter(
                DBUser.enrollment_number == enrollment_number
            ).first()

        if existing_user:
            return None

        user = DBUser(
            username=username,
            enrollment_number=enrollment_number,
            password_hash=generate_password_hash(password),
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception:
        db.rollback()
        return None


def verify_user(db, username, password):
    user = db.query(DBUser).filter(DBUser.username == username).first()

    if user and check_password_hash(user.password_hash, password):
        return user

    return None
