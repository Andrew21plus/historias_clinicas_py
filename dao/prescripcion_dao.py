from models.prescripcion import Prescripcion
from dao.database import get_connection  # Importar get_connection

def get_all_prescripciones():
    conn = get_connection()  # Usar get_connection
    c = conn.cursor()
    c.execute("SELECT * FROM Prescripciones")
    rows = c.fetchall()
    prescripciones = [Prescripcion(*row) for row in rows]
    conn.close()
    return prescripciones

def get_prescripcion_by_id(id_prescripcion):
    conn = get_connection()  # Usar get_connection
    c = conn.cursor()
    c.execute("SELECT * FROM Prescripciones WHERE id_prescripcion = ?", (id_prescripcion,))
    row = c.fetchone()
    conn.close()
    return Prescripcion(*row) if row else None

def add_prescripcion(id_paciente, fecha, medicamento, dosis, indicaciones, firmado_por, id_usuario):
    conn = get_connection()  # Usar get_connection
    c = conn.cursor()
    c.execute("""
        INSERT INTO Prescripciones (id_paciente, fecha, medicamento, dosis, indicaciones, firmado_por, id_usuario)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (id_paciente, fecha, medicamento, dosis, indicaciones, firmado_por, id_usuario))
    conn.commit()
    conn.close()

def update_prescripcion(id_prescripcion, fecha, medicamento, dosis, indicaciones, firmado_por):
    conn = get_connection()  # Usar get_connection
    c = conn.cursor()
    c.execute("""
        UPDATE Prescripciones 
        SET fecha = ?, medicamento = ?, dosis = ?, indicaciones = ?, firmado_por = ?
        WHERE id_prescripcion = ?
    """, (fecha, medicamento, dosis, indicaciones, firmado_por, id_prescripcion))
    conn.commit()
    conn.close()

def delete_prescripcion(id_prescripcion):
    conn = get_connection()  # Usar get_connection
    c = conn.cursor()
    c.execute("DELETE FROM Prescripciones WHERE id_prescripcion = ?", (id_prescripcion,))
    conn.commit()
    conn.close()

def get_prescripciones_by_paciente_and_fecha(id_paciente, fecha):
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT * FROM Prescripciones 
        WHERE id_paciente = ? AND fecha = ?
        ORDER BY fecha DESC
    """, (id_paciente, fecha))
    rows = c.fetchall()
    prescripciones = [Prescripcion(*row) for row in rows]
    conn.close()
    return prescripciones

def get_prescripciones_by_usuario(id_usuario):
    conn = get_connection()  # Obtener la conexión a la base de datos
    c = conn.cursor()
    # Consulta para obtener todas las historias clínicas asociadas a un usuario específico
    c.execute("SELECT * FROM Prescripciones WHERE id_usuario = ?", (id_usuario,))
    rows = c.fetchall()
    # Convertir las filas en objetos HistoriaClinica
    prescripciones = [Prescripcion(*row) for row in rows]
    conn.close()
    return prescripciones