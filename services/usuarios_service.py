from dao.usuarios_dao import get_usuario, crear_usuario
import bcrypt


def validar_usuario(correo, password):
    """Valida si el usuario y contraseña son correctos"""
    user_data = get_usuario(correo)

    if user_data is not None:  # user_data es un objeto Usuario
        id_usuario = user_data.id_usuario
        nombre = user_data.nombre
        apellido = user_data.apellido
        hashed_password = user_data.contrasena  # Campo de la contraseña en la BD

        if bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8")):
            return {
                "status": True,
                "message": "Inicio de sesión exitoso",
                "id_usuario": id_usuario,
                "nombre": nombre,
                "apellido": apellido,
                "correo": correo,
            }
        else:
            return {"status": False, "message": "Contraseña incorrecta"}

    return {"status": False, "message": "Usuario no encontrado"}

# Funcion para crear usuario
def nuevo_usuario(nombre, apellido, correo, contrasena):
    """Crea un nuevo usuario en la base de datos"""
    return crear_usuario(nombre, apellido, correo, contrasena)
