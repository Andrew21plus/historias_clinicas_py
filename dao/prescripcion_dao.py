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

def add_prescripcion(id_paciente, fecha, medicamento, dosis, indicaciones, firmado_por):
    conn = get_connection()  # Usar get_connection
    c = conn.cursor()
    c.execute("""
        INSERT INTO Prescripciones (id_paciente, fecha, medicamento, dosis, indicaciones, firmado_por)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (id_paciente, fecha, medicamento, dosis, indicaciones, firmado_por))
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