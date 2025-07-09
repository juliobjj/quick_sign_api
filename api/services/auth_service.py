from sqlalchemy.orm import Session
from api.model.usuario_model import UsuarioModel
from flask_jwt_extended import create_access_token
from datetime import timedelta

class AuthService:
  def __init__(self, db_session: Session):
      self.db_session = db_session

  def authenticate_user(self, email: str, password: str) -> str | None:
      user = self.db_session.query(UsuarioModel).filter_by(email=email).first()
      if user and user.verify_password(password):
          expires = timedelta(hours=1)
          access_token = create_access_token(identity=str(user.id), expires_delta=expires)
          return access_token
      return None
