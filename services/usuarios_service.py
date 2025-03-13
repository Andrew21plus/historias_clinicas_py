from dao.usuarios_dao import get_usuario, crear_usuario
import bcrypt


def validar_usuario(correo, password):
    """Valida si el usuario y contraseña son correctos"""
    user_data = get_usuario(correo)
    print("[login_service] user_data:", user_data)
    print("[login_service] type(user_data):", type(user_data))

    if user_data is not None:
        id_usuario, nombre, apellido, hashed_password, rol = user_data
        if bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8")):
            return {
                "status": True,
                "message": "Inicio de sesión exitoso",
                "id_usuario": id_usuario,
                "nombre": nombre,
                "apellido": apellido,
                "correo": correo,
                "rol": rol,
            }
        else:
            return {"status": False, "message": "Contraseña incorrecta"}

    return {"status": False, "message": "Usuario no encontrado"}


# Funcion para crear usuario
def nuevo_usuario(nombre, apellido, correo, contrasena, rol):
    """Crea un nuevo usuario en la base de datos"""
    return crear_usuario(nombre, apellido, correo, contrasena, rol)
