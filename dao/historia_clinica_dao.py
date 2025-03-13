from models.historia_clinica import HistoriaClinica
from dao.database import get_connection  # Importar get_connection

def get_all_historias_clinicas():
    conn = get_connection()  # Usar get_connection
    c = conn.cursor()
    c.execute("SELECT * FROM Historias_Clinicas")
    rows = c.fetchall()
    historias = [HistoriaClinica(*row) for row in rows]
    conn.close()
    return historias

def get_historia_clinica_by_id(id_historia):
    conn = get_connection()  # Usar get_connection
    c = conn.cursor()
    c.execute("SELECT * FROM Historias_Clinicas WHERE id_historia = ?", (id_historia,))
    row = c.fetchone()
    conn.close()
    return HistoriaClinica(*row) if row else None

def add_historia_clinica(id_paciente, motivo_consulta, enfermedad_actual, id_usuario):
    conn = get_connection()  # Usar get_connection
    c = conn.cursor()
    c.execute("""
        INSERT INTO Historias_Clinicas (id_paciente, motivo_consulta, enfermedad_actual, id_usuario)
        VALUES (?, ?, ?, ?)
    """, (id_paciente, motivo_consulta, enfermedad_actual,id_usuario))
    conn.commit()
    conn.close()

def update_historia_clinica(id_historia, motivo_consulta, enfermedad_actual, id_usuario):
    conn = get_connection()  # Usar get_connection
    c = conn.cursor()
    c.execute("""
        UPDATE Historias_Clinicas 
        SET motivo_consulta = ?, enfermedad_actual = ?
        WHERE id_historia = ?
    """, (motivo_consulta, enfermedad_actual, id_historia, id_usuario))
    conn.commit()
    conn.close()

def delete_historia_clinica(id_historia):
    conn = get_connection()  # Usar get_connection
    c = conn.cursor()
    c.execute("DELETE FROM Historias_Clinicas WHERE id_historia = ?", (id_historia,))
    conn.commit()
    conn.close()

def get_historia_clinica_by_paciente(id_paciente):
    conn = get_connection()  # Usar get_connection
    c = conn.cursor()
    c.execute("SELECT * FROM Historias_Clinicas WHERE id_paciente = ?", (id_paciente,))
    row = c.fetchone()
    conn.close()
    return row  # Devuelve la historia clínica si existe, o None si no existe

def get_historias_clinicas_by_usuario(id_usuario):
    conn = get_connection()  # Obtener la conexión a la base de datos
    c = conn.cursor()
    # Consulta para obtener todas las historias clínicas asociadas a un usuario específico
    c.execute("SELECT * FROM Historias_Clinicas WHERE id_usuario = ?", (id_usuario,))
    rows = c.fetchall()
    # Convertir las filas en objetos HistoriaClinica
    historias = [HistoriaClinica(*row) for row in rows]
    conn.close()
    return historias