import json
from models.paciente import Paciente
from dao.database import get_connection  # Importar get_connection


def get_all_pacientes():
    """Obtiene todos los pacientes de la base de datos"""
    conn = get_connection()  # Usar get_connection en lugar de sqlite3.connect
    c = conn.cursor()
    c.execute(
        "SELECT id_paciente, nombre, apellido, sexo, fecha_nacimiento, num_historia_clinica, foto, id_usuario FROM Pacientes"
    )

    rows = c.fetchall()
    pacientes = [Paciente(*row) for row in rows]
    pacientes_dict = [
        {
            k: (str(v)[:60] + "..." if len(str(v)) > 60 else str(v))
            for k, v in paciente.__dict__.items()
        }
        for paciente in pacientes
    ]

    # Imprimimos el contenido con formato JSON
    print(f"\n\n[pacientes_dao] type pacientes: {type(pacientes)}")
    print(
        f"[pacientes_dao] contenido pacientes: {json.dumps(pacientes_dict, indent=2, ensure_ascii=False)}"
    )
    conn.close()
    return pacientes


def get_pacientes_id_usuario(id_usuario):
    """Obtiene todos los pacientes de un usuario específico por su id_usuario"""
    conn = get_connection()  # Usar get_connection en lugar de sqlite3.connect
    c = conn.cursor()
    c.execute(
        "SELECT id_paciente, nombre, apellido, sexo, fecha_nacimiento, num_historia_clinica, foto, id_usuario FROM Pacientes WHERE id_usuario = ?",
        (id_usuario,),
    )

    rows = c.fetchall()
    pacientes = [Paciente(*row) for row in rows]
    pacientes_dict = [
        {
            k: (str(v)[:60] + "..." if len(str(v)) > 60 else str(v))
            for k, v in paciente.__dict__.items()
        }
        for paciente in pacientes
    ]

    # Imprimimos el contenido con formato JSON
    print(f"\n\n[pacientes_dao] type pacientes: {type(pacientes)}")
    print(
        f"[pacientes_dao] contenido pacientes: {json.dumps(pacientes_dict, indent=2, ensure_ascii=False)}"
    )
    conn.close()
    return pacientes


def get_paciente_by_id(id_paciente):
    """Obtiene un paciente por su ID"""
    conn = get_connection()  # Usar get_connection en lugar de sqlite3.connect
    c = conn.cursor()
    c.execute("SELECT * FROM Pacientes WHERE id_paciente = ?", (id_paciente,))
    row = c.fetchone()
    conn.close()
    return Paciente(*row) if row else None


def add_paciente(
    id_paciente,
    nombre,
    apellido,
    sexo,
    fecha_nacimiento,
    num_historia_clinica,
    foto,
    id_usuario,
):
    print(
        f"\n\n[paciente_dao] Valores: id_paciente: {id_paciente}, nombre: {nombre}, apellido: {apellido}, sexo: {sexo}, fecha_nacimiento: {fecha_nacimiento}, num_historia_clinica: {num_historia_clinica}, id_usuario: {id_usuario}, foto: {foto}"
    )
    """Agrega un nuevo paciente a la base de datos"""
    conn = get_connection()  # Usar get_connection en lugar de sqlite3.connect
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO Pacientes (id_paciente, nombre, apellido, sexo, fecha_nacimiento, num_historia_clinica, foto, id_usuario)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            id_paciente,
            nombre,
            apellido,
            sexo,
            fecha_nacimiento,
            num_historia_clinica,
            foto,
            id_usuario,
        ),
    )
    conn.commit()
    conn.close()


def update_paciente(
    id_paciente,
    nombre,
    apellido,
    sexo,
    fecha_nacimiento,
    num_historia_clinica,
    id_usuario,
    foto,
):
    print(
        f"\n\n[paciente_dao] update_paciente: id_paciente: {id_paciente}, nombre: {nombre}, apellido: {apellido}, sexo: {sexo}, fecha_nacimiento: {fecha_nacimiento}, num_historia_clinica: {num_historia_clinica}, id_usuario: {id_usuario}, foto: {foto}"
    )
    """Actualiza los datos de un paciente"""
    conn = get_connection()  # Usar get_connection en lugar de sqlite3.connect
    c = conn.cursor()
    c.execute(
        """
        UPDATE Pacientes 
        SET nombre = ?, apellido = ?, sexo = ?, fecha_nacimiento = ?, num_historia_clinica = ?, foto = ?, id_usuario = ?
        WHERE id_paciente = ?
    """,
        (
            nombre,
            apellido,
            sexo,
            fecha_nacimiento,
            num_historia_clinica,
            foto,
            id_usuario,
            id_paciente,
        ),
    )
    conn.commit()
    conn.close()


def delete_paciente(id_paciente):
    """Elimina un paciente por su ID"""
    conn = get_connection()  # Usar get_connection en lugar de sqlite3.connect
    c = conn.cursor()
    c.execute("DELETE FROM Pacientes WHERE id_paciente = ?", (id_paciente,))
    conn.commit()
    conn.close()
