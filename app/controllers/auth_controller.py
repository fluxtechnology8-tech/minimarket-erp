from services.auth_service import AuthService


class AuthController:
    def __init__(self, auth_service: AuthService = None):
        self.service = auth_service or AuthService()

    def login(self, username: str, password: str) -> dict | None:
        """
        Maneja el proceso de login del usuario.
        
        Args:
            username: Nombre de usuario
            password: Contraseña del usuario
            
        Returns:
            dict con datos del usuario si el login es exitoso, None en caso contrario
        """
        try:
            usuario = self.service.autenticar(username, password)
            return usuario
        except ValueError as e:
            raise ValueError(f"Error en autenticación: {str(e)}")

    def get_usuario(self, usuario_id: int) -> dict | None:
        """
        Obtiene los datos de un usuario por su ID.
        
        Args:
            usuario_id: ID del usuario
            
        Returns:
            dict con datos del usuario o None si no existe
        """
        return self.service.get_usuario_by_id(usuario_id)

    def listar_usuarios(self) -> list[dict]:
        """
        Lista todos los usuarios del sistema.
        
        Returns:
            Lista de diccionarios con datos de usuarios
        """
        return self.service.get_all_usuarios()

    def crear_usuario(self, data: dict) -> dict:
        """
        Crea un nuevo usuario en el sistema.
        
        Args:
            data: Diccionario con datos del usuario
            
        Returns:
            dict con el resultado de la operación
        """
        return self.service.crear_usuario(data)

    def actualizar_usuario(self, usuario_id: int, data: dict) -> dict:
        """
        Actualiza los datos de un usuario.
        
        Args:
            usuario_id: ID del usuario a actualizar
            data: Diccionario con datos a actualizar
            
        Returns:
            dict con el resultado de la operación
        """
        return self.service.actualizar_usuario(usuario_id, data)

    def eliminar_usuario(self, usuario_id: int) -> bool:
        """
        Elimina (desactiva) un usuario del sistema.
        
        Args:
            usuario_id: ID del usuario a eliminar
            
        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        return self.service.eliminar_usuario(usuario_id)
