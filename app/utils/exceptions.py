class NotFoundException(Exception):
    """Cuando un recurso no se encuentra"""
    pass

class AuthException(Exception):
    """Errores relacionados con autenticación"""
    pass

class PermissionException(Exception):
    """Errores de permisos"""
    pass