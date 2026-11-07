"""Validación y saneamiento de entradas de usuario.

Este módulo centraliza las reglas de validación para evitar inyecciones,
datos mal formados y exposición de información sensible.
"""
import re
import html
from datetime import datetime


def sanitizar_texto(valor, max_len=255):
    """Elimina espacios extremos, caracteres de control y limita la longitud."""
    if valor is None:
        return ""
    if not isinstance(valor, str):
        valor = str(valor)
    valor = valor.strip()
    # Eliminar caracteres de control y no imprimibles
    valor = "".join(ch for ch in valor if ch.isprintable())
    # Escapar HTML para evitar XSS si los datos se muestran en otros contextos
    valor = html.escape(valor)
    if len(valor) > max_len:
        valor = valor[:max_len]
    return valor


def validar_no_vacio(valor, campo="campo"):
    if not valor or not str(valor).strip():
        return False, f"El {campo} es obligatorio."
    return True, ""


def validar_email(email):
    email = (email or "").strip()
    patron = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    if not re.fullmatch(patron, email):
        return False, "Email inválido. Formato esperado: usuario@dominio.com"
    return True, ""


def validar_telefono(telefono):
    limpio = (telefono or "").replace(" ", "").replace("-", "")
    if not re.fullmatch(r"^\+?\d{8,15}$", limpio):
        return False, "Teléfono inválido. Use solo dígitos (8 a 15), opcional '+'."
    return True, ""


def validar_nombre(nombre):
    nombre = (nombre or "").strip()
    if len(nombre) < 2 or len(nombre) > 100:
        return False, "El nombre debe tener entre 2 y 100 caracteres."
    if not re.fullmatch(r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s\.\-]+$", nombre):
        return False, "El nombre solo puede contener letras, espacios, puntos y guiones."
    return True, ""


def validar_entero_positivo(valor, campo="valor"):
    try:
        n = int(valor)
    except (ValueError, TypeError):
        return False, f"{campo} debe ser un número entero."
    if n <= 0:
        return False, f"{campo} debe ser mayor a 0."
    return True, ""


def validar_float_positivo(valor, campo="valor"):
    try:
        n = float(valor)
    except (ValueError, TypeError):
        return False, f"{campo} debe ser un número."
    if n <= 0:
        return False, f"{campo} debe ser mayor a 0."
    return True, ""


def validar_salario(valor):
    ok, msg = validar_float_positivo(valor, "salario")
    if not ok:
        return ok, msg
    if float(valor) > 1_000_000_000:
        return False, "Salario fuera de rango permitido."
    return True, ""


def validar_fecha(fecha_str, formato="%Y-%m-%d"):
    try:
        datetime.strptime(fecha_str, formato)
        return True, ""
    except (ValueError, TypeError):
        return False, f"Fecha inválida. Formato esperado: {formato}."


def validar_ciudad(ciudad):
    ciudad = (ciudad or "").strip()
    if len(ciudad) < 2 or len(ciudad) > 80:
        return False, "Ciudad inválida."
    if not re.fullmatch(r"^[A-Za-zÁÉÍÓÚáéíóúÑñÜü\s\.\-]+$", ciudad):
        return False, "La ciudad solo puede contener letras, espacios, puntos y guiones."
    return True, ""


def validar_codigo_moneda(codigo):
    codigo = (codigo or "").strip().upper()
    if not re.fullmatch(r"^[A-Z]{3}$", codigo):
        return False, "Código de moneda inválido (3 letras, ej: USD, CLP, EUR)."
    return True, ""


def validar_username(username):
    username = (username or "").strip()
    if len(username) < 3 or len(username) > 30:
        return False, "El usuario debe tener entre 3 y 30 caracteres."
    if not re.fullmatch(r"^[A-Za-z0-9_.-]+$", username):
        return False, "El usuario solo puede contener letras, números, punto, guion y guion bajo."
    return True, ""


def validar_password(password):
    password = password or ""
    if len(password) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres."
    if not re.search(r"[A-Z]", password):
        return False, "La contraseña debe incluir al menos una mayúscula."
    if not re.search(r"[a-z]", password):
        return False, "La contraseña debe incluir al menos una minúscula."
    if not re.search(r"\d", password):
        return False, "La contraseña debe incluir al menos un número."
    return True, ""


def validar_rol(rol):
    roles_validos = {"Administrador", "Gerente", "Empleado", "Lector"}
    if rol not in roles_validos:
        return False, f"Rol inválido. Roles permitidos: {', '.join(sorted(roles_validos))}."
    return True, ""


def leer_entero_seguro(mensaje, minimo=None, maximo=None):
    """Lee un entero de consola con validación."""
    while True:
        valor = input(mensaje).strip()
        try:
            n = int(valor)
        except ValueError:
            print("Error: Ingrese un número entero válido.")
            continue
        if minimo is not None and n < minimo:
            print(f"Error: El valor debe ser >= {minimo}.")
            continue
        if maximo is not None and n > maximo:
            print(f"Error: El valor debe ser <= {maximo}.")
            continue
        return n


def leer_float_seguro(mensaje, minimo=None, maximo=None):
    while True:
        valor = input(mensaje).strip()
        try:
            n = float(valor)
        except ValueError:
            print("Error: Ingrese un valor numérico válido.")
            continue
        if minimo is not None and n < minimo:
            print(f"Error: El valor debe ser >= {minimo}.")
            continue
        if maximo is not None and n > maximo:
            print(f"Error: El valor debe ser <= {maximo}.")
            continue
        return n
