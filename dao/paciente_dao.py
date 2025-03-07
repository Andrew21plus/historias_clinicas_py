from models.paciente import Paciente
from dao.database import DB_NAME, get_connection  # Importar get_connection

def get_all_pacientes():
    """ Obtiene todos los pacientes de la base de datos """
    conn = get_connection()  # Usar get_connection en lugar de sqlite3.connect
    c = conn.cursor()
    c.execute("SELECT * FROM Pacientes")
    rows = c.fetchall()
    pacientes = [Paciente(*row) for row in rows]
    conn.close()
    return pacientes

def get_paciente_by_id(id_paciente):
    """ Obtiene un paciente por su ID """
    conn = get_connection()  # Usar get_connection en lugar de sqlite3.connect
    c = conn.cursor()
    c.execute("SELECT * FROM Pacientes WHERE id_paciente = ?", (id_paciente,))
    row = c.fetchone()
    conn.close()
    return Paciente(*row) if row else None

def add_paciente(id_paciente, nombre, apellido, sexo, fecha_nacimiento, num_historia_clinica, foto=None):
    """ Agrega un nuevo paciente a la base de datos """
    conn = get_connection()  # Usar get_connection en lugar de sqlite3.connect
    c = conn.cursor()
    c.execute("""
        INSERT INTO Pacientes (id_paciente, nombre, apellido, sexo, fecha_nacimiento, num_historia_clinica, foto)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (id_paciente, nombre, apellido, sexo, fecha_nacimiento, num_historia_clinica, foto))
    conn.commit()
    conn.close()

def update_paciente(id_paciente, nombre, apellido, sexo, fecha_nacimiento, num_historia_clinica, foto=None):
    """ Actualiza los datos de un paciente """
    conn = get_connection()  # Usar get_connection en lugar de sqlite3.connect
    c = conn.cursor()
    c.execute("""
        UPDATE Pacientes 
        SET nombre = ?, apellido = ?, sexo = ?, fecha_nacimiento = ?, num_historia_clinica = ?, foto = ?
        WHERE id_paciente = ?
    """, (nombre, apellido, sexo, fecha_nacimiento, num_historia_clinica, foto, id_paciente))
    conn.commit()
    conn.close()

def delete_paciente(id_paciente):
    """ Elimina un paciente por su ID """
    conn = get_connection()  # Usar get_connection en lugar de sqlite3.connect
    c = conn.cursor()
    c.execute("DELETE FROM Pacientes WHERE id_paciente = ?", (id_paciente,))
    conn.commit()
    conn.close()