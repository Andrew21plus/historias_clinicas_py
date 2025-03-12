from dao.database import get_connection  # Importar conexión a la BD
import bcrypt


def get_usuario(correo):
    """Busca un usuario en la base de datos por su correo"""
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "SELECT nombre, apellido, contrasena, rol FROM Usuarios WHERE correo = ?",
        (correo,),
    )
    row = c.fetchone()
    conn.close()
    return row


def crear_usuario(nombre, apellido, correo, contrasena, rol):
    """Crea un nuevo usuario en la base de datos y devuelve un diccionario con la respuesta"""
    conn = get_connection()
    c = conn.cursor()

    # Verificar si el correo ya existe
    c.execute("SELECT * FROM Usuarios WHERE correo = ?", (correo,))
    if c.fetchone():
        conn.close()
        return {"status": "error", "message": "El correo ya está registrado."}

    # Encriptar la contraseña
    contrasena_hash = bcrypt.hashpw(
        contrasena.encode("utf-8"), bcrypt.gensalt()
    ).decode("utf-8")

    try:
        c.execute(
            "INSERT INTO Usuarios (nombre, apellido, correo, contrasena, rol) VALUES (?, ?, ?, ?, ?)",
            (nombre, apellido, correo, contrasena_hash, rol),
        )
        conn.commit()
        return {"status": "success", "message": "Usuario creado exitosamente."}
    except Exception as e:
        return {"status": "error", "message": f"Error al crear usuario: {e}"}
    finally:
        conn.close()
