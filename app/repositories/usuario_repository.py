from core.database import get_session_manager
from models.usuario import Usuario


class UsuarioRepository:
    def __init__(self, session_manager=None):
        self._sm = session_manager or get_session_manager()

    def autenticar(self, username: str, password: str) -> dict | None:
        with self._sm.get_session() as session:
            usuario = (
                session.query(Usuario)
                .filter(
                    Usuario.username == username,
                    Usuario.password == password,
                    Usuario.activo == 1,
                )
                .first()
            )
            return self._to_dict(usuario) if usuario else None

    def get_by_id(self, usuario_id: int) -> dict | None:
        with self._sm.get_session() as session:
            usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()
            return self._to_dict(usuario) if usuario else None

    def get_all(self) -> list[dict]:
        with self._sm.get_session() as session:
            usuarios = session.query(Usuario).order_by(Usuario.nombre).all()
            return [self._to_dict(u) for u in usuarios]

    def create(self, data: dict) -> int:
        with self._sm.get_session() as session:
            usuario = Usuario(
                username=data["username"],
                password=data["password"],
                nombre=data["nombre"],
                rol=data["rol"],
            )
            session.add(usuario)
            session.flush()
            return usuario.id

    def update(self, usuario_id: int, data: dict) -> dict:
        with self._sm.get_session() as session:
            usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()
            if not usuario:
                raise ValueError("Usuario no encontrado.")

            if "nombre" in data:
                usuario.nombre = data["nombre"]
            if "username" in data:
                usuario.username = data["username"]
            if "password" in data:
                usuario.password = data["password"]
            if "rol" in data:
                usuario.rol = data["rol"]

            return {"success": True, "id": usuario_id}

    def delete(self, usuario_id: int) -> bool:
        with self._sm.get_session() as session:
            usuario = session.query(Usuario).filter(Usuario.id == usuario_id).first()
            if usuario:
                usuario.activo = 0
                return True
            return False

    def _to_dict(self, u: Usuario) -> dict:
        return {
            "id": u.id,
            "username": u.username,
            "nombre": u.nombre,
            "rol": u.rol,
            "activo": u.activo,
            "fecha_creacion": u.fecha_creacion,
        }
