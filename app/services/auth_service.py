from repositories.usuario_repository import UsuarioRepository


class AuthService:
    def __init__(self, usuario_repo: UsuarioRepository = None):
        self.usuario_repo = usuario_repo or UsuarioRepository()

    def autenticar(self, username: str, password: str) -> dict | None:
        """
        Autentica un usuario validando sus credenciales.
        
        Args:
            username: Nombre de usuario
            password: Contraseña del usuario
            
        Returns:
            dict con datos del usuario si es válido, None si no existe o credenciales incorrectas
        """
        if not username or not password:
            raise ValueError("Usuario y contraseña son requeridos")
        
        usuario = self.usuario_repo.autenticar(username, password)
        return usuario

    def get_usuario_by_id(self, usuario_id: int) -> dict | None:
        """
        Obtiene los datos de un usuario por su ID.
        
        Args:
            usuario_id: ID del usuario
            
        Returns:
            dict con datos del usuario o None si no existe
        """
        return self.usuario_repo.get_by_id(usuario_id)

    def get_all_usuarios(self) -> list[dict]:
        """
        Obtiene todos los usuarios del sistema.
        
        Returns:
            Lista de diccionarios con datos de usuarios
        """
        return self.usuario_repo.get_all()

    def crear_usuario(self, data: dict) -> dict:
        """
        Crea un nuevo usuario en el sistema.
        
        Args:
            data: Diccionario con datos del usuario (username, password, nombre, rol)
            
        Returns:
            dict con el resultado de la operación
        """
        # Validar datos requeridos
        if not data.get("username"):
            raise ValueError("El username es obligatorio")
        if not data.get("password"):
            raise ValueError("La contraseña es obligatoria")
        if not data.get("nombre"):
            raise ValueError("El nombre es obligatorio")
        if not data.get("rol"):
            raise ValueError("El rol es obligatorio")

        usuario_id = self.usuario_repo.create(data)
        return {"success": True, "id": usuario_id}

    def actualizar_usuario(self, usuario_id: int, data: dict) -> dict:
        """
        Actualiza los datos de un usuario.
        
        Args:
            usuario_id: ID del usuario a actualizar
            data: Diccionario con datos a actualizar
            
        Returns:
            dict con el resultado de la operación
        """
        return self.usuario_repo.update(usuario_id, data)

    def eliminar_usuario(self, usuario_id: int) -> bool:
        """
        Elimina (desactiva) un usuario del sistema.
        
        Args:
            usuario_id: ID del usuario a eliminar
            
        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        return self.usuario_repo.delete(usuario_id)
