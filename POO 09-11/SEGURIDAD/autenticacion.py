"""Autenticación y gestión de usuarios con contraseñas cifradas (hash)."""
import hashlib
import hmac
import secrets
import os

from SEGURIDAD.validaciones import (
    sanitizar_texto,
    validar_username,
    validar_password,
    validar_rol,
)
from DTO.usuario_dto import UsuarioDTO
from DAO.usuario_dao import UsuarioDAO


def hash_password(password, salt=None):
    """Genera un hash seguro con salt usando PBKDF2-HMAC-SHA256."""
    if salt is None:
        salt = secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), 100_000
    ).hex()
    return f"{salt}${hashed}"


def verificar_password(password, stored_hash):
    """Verifica una contraseña contra un hash almacenado (comparación segura)."""
    if not stored_hash or "$" not in stored_hash:
        return False
    salt, _ = stored_hash.split("$", 1)
    nuevo = hash_password(password, salt)
    return hmac.compare_digest(nuevo, stored_hash)


class AutenticacionService:
    """Servicio de login y gestión de usuarios."""

    def __init__(self):
        self.dao = UsuarioDAO()
        self._asegurar_admin_por_defecto()

    def _asegurar_admin_por_defecto(self):
        """Crea un usuario administrador inicial si no existe ninguno."""
        try:
            if self.dao.contar() == 0:
                password_inicial = os.getenv("ADMIN_INITIAL_PASSWORD", "Admin123!")
                dto = UsuarioDTO(
                    username="admin",
                    password_hash=hash_password(password_inicial),
                    rol="Administrador",
                    empleado_id=None,
                )
                self.dao.guardar(dto)
                print("\n[SEGURIDAD] Se creó el usuario inicial 'admin'.")
                print(f"[SEGURIDAD] Contraseña inicial: {password_inicial}")
                print("[SEGURIDAD] Cámbiela después del primer ingreso.\n")
        except Exception as e:
            # No interrumpir la aplicación si la BD no está disponible
            print(f"[SEGURIDAD] No se pudo verificar/crear usuario admin: {e}")

    def login(self, username, password):
        """Autentica un usuario. Retorna el DTO si es válido, None si no."""
        username = sanitizar_texto(username, 30)
        if not username or not password:
            return None
        try:
            usuario = self.dao.buscar_por_username(username)
        except Exception:
            return None
        if usuario is None:
            return None
        if verificar_password(password, usuario.password_hash):
            return usuario
        return None

    def registrar_usuario(self, username, password, rol, empleado_id=None):
        """Registra un nuevo usuario validando entradas."""
        ok, msg = validar_username(username)
        if not ok:
            raise ValueError(msg)
        ok, msg = validar_password(password)
        if not ok:
            raise ValueError(msg)
        ok, msg = validar_rol(rol)
        if not ok:
            raise ValueError(msg)

        username = sanitizar_texto(username, 30)
        if self.dao.buscar_por_username(username) is not None:
            raise ValueError("El nombre de usuario ya existe.")

        dto = UsuarioDTO(
            username=username,
            password_hash=hash_password(password),
            rol=rol,
            empleado_id=empleado_id,
        )
        return self.dao.guardar(dto)

    def cambiar_password(self, username, password_actual, password_nuevo):
        usuario = self.dao.buscar_por_username(sanitizar_texto(username, 30))
        if usuario is None:
            return False, "Usuario no encontrado."
        if not verificar_password(password_actual, usuario.password_hash):
            return False, "La contraseña actual es incorrecta."
        ok, msg = validar_password(password_nuevo)
        if not ok:
            return False, msg
        nuevo_hash = hash_password(password_nuevo)
        if self.dao.actualizar_password(usuario.id_usuario, nuevo_hash):
            return True, "Contraseña actualizada correctamente."
        return False, "No se pudo actualizar la contraseña."

    def tiene_permiso(self, usuario, modulo):
        """Control básico de acceso por rol."""
        if usuario is None:
            return False
        rol = getattr(usuario, "rol", "Empleado")
        if rol == "Administrador":
            return True
        permisos = {
            "Gerente": {"empleados", "departamentos", "proyectos", "asignaciones", "registros", "api"},
            "Empleado": {"proyectos", "registros", "api"},
            "Lector": {"api"},
        }
        return modulo in permisos.get(rol, set())
