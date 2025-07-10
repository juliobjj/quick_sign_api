from ..base import db 
from datetime import datetime
from passlib.hash import bcrypt

class UsuarioModel(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def verify_password(self, password: str) -> bool:
        return bcrypt.verify(password, self.password_hash)

    @classmethod
    def create_with_password(cls, email: str, password: str):
        return cls(
            email=email,
            password_hash=bcrypt.hash(password)
        )