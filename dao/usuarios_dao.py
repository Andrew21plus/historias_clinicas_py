from dao.database import get_connection  # Importar conexión a la BD
import bcrypt
from models.usuario import Usuario  # Importar la clase Usuario


def get_usuario(correo):
    """Busca un usuario en la base de datos por su correo y devuelve una instancia de Usuario"""
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "SELECT id_usuario, nombre, apellido, correo, contrasena FROM Usuarios WHERE correo = ?",
        (correo,),
    )
    row = c.fetchone()
    conn.close()

    if row:
        # Crear una instancia de Usuario con los datos obtenidos
        return Usuario(
            id_usuario=row[0],
            nombre=row[1],
            apellido=row[2],
            correo=row[3],
            contrasena=row[4],
        )
    return None  # Si no se encuentra el usuario, devolver None


def crear_usuario(nombre, apellido, correo, contrasena):
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
            "INSERT INTO Usuarios (nombre, apellido, correo, contrasena) VALUES (?, ?, ?, ?)",
            (nombre, apellido, correo, contrasena_hash),
        )
        conn.commit()

        # Obtener el ID del usuario recién creado
        usuario_id = c.lastrowid

        # Crear una instancia de Usuario con los datos del nuevo usuario
        nuevo_usuario = Usuario(
            id_usuario=usuario_id,
            nombre=nombre,
            apellido=apellido,
            correo=correo,
            contrasena=contrasena_hash,
        )

        return {"status": "success", "message": "Usuario creado exitosamente.", "usuario": nuevo_usuario}
    except Exception as e:
        return {"status": "error", "message": f"Error al crear usuario: {e}"}
    finally:
        conn.close()