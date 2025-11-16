import sqlalchemy
import sqlalchemy.orm
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "data.db")

engine = sqlalchemy.create_engine(f"sqlite:///{DB_PATH}", echo=False)
SessionLocal = sqlalchemy.orm.sessionmaker(bind=engine)
Base = sqlalchemy.orm.declarative_base()

class User(Base):
    __tablename__ = "users"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    token = sqlalchemy.Column(sqlalchemy.String, unique=True, index=True)
    files = sqlalchemy.orm.relationship("File", back_populates="user", cascade="all, delete")

class File(Base):
    __tablename__ = "files"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    filepath = sqlalchemy.Column(sqlalchemy.String)
    content = sqlalchemy.Column(sqlalchemy.Text)
    user = sqlalchemy.orm.relationship("User", back_populates="files")

def get_or_make_user(token):
    db = SessionLocal()
    user = db.query(User).filter_by(token=token).first()
    if not user:
        user = User(token=token)
        db.add(user)
        db.commit()
    files = db.query(File).filter_by(user_id=user.id).all()
    result = [{"filepath": f.filepath, "content": f.content} for f in files]
    db.close()
    return result

def save_file(token, filepath, content):
    db = SessionLocal()
    user = db.query(User).filter_by(token=token).first()
    if not user:
        user = get_or_make_user(token)

    file = db.query(File).filter_by(user_id=user.id, filepath=filepath).first()
    if file:
        file.content = content
    else:
        file = File(user_id=user.id, filepath=filepath, content=content)
        db.add(file)
    db.commit()
    db.close()

def load_file(token, filepath):
    db = SessionLocal()
    user = db.query(User).filter_by(token=token).first()
    if not user:
        db.close()
        return None
    file = db.query(File).filter_by(user_id=user.id, filepath=filepath).first()
    db.close()
    return file.content if file else None

def clear_user(token):
    db = SessionLocal()
    user = db.query(User).filter_by(token=token).first()
    if user:
        db.query(File).filter_by(user_id=user.id).delete()
    db.commit()
    db.close()

Base.metadata.create_all(engine)