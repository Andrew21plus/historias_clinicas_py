from models.signo_vital import SignoVital
from dao.database import get_connection  # Importar get_connection


def get_all_signos_vitales():
    conn = get_connection()  # Usar get_connection
    c = conn.cursor()
    c.execute("SELECT * FROM Signos_Vitales")
    rows = c.fetchall()
    signos = [SignoVital(*row) for row in rows]
    conn.close()
    return signos


def get_signo_vital_by_id(id_signo):
    conn = get_connection()  # Usar get_connection
    c = conn.cursor()
    c.execute("SELECT * FROM Signos_Vitales WHERE id_signo = ?", (id_signo,))
    row = c.fetchone()
    conn.close()
    return SignoVital(*row) if row else None


def add_signo_vital(
    id_paciente,
    fecha,
    presion_arterial,
    frecuencia_cardiaca,
    frecuencia_respiratoria,
    temperatura,
    peso,
    talla,
):
    conn = get_connection()  # Usar get_connection
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO Signos_Vitales (id_paciente, fecha, presion_arterial, frecuencia_cardiaca, frecuencia_respiratoria, temperatura, peso, talla)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
        (
            id_paciente,
            fecha,
            presion_arterial,
            frecuencia_cardiaca,
            frecuencia_respiratoria,
            temperatura,
            peso,
            talla,
        ),
    )
    conn.commit()
    conn.close()


def update_signo_vital(
    id_signo,
    fecha,
    presion_arterial,
    frecuencia_cardiaca,
    frecuencia_respiratoria,
    temperatura,
    peso,
    talla,
):
    conn = get_connection()  # Usar get_connection
    c = conn.cursor()
    c.execute(
        """
        UPDATE Signos_Vitales 
        SET fecha = ?, presion_arterial = ?, frecuencia_cardiaca = ?, frecuencia_respiratoria = ?, temperatura = ?, peso = ?, talla = ?
        WHERE id_signo = ?
    """,
        (
            fecha,
            presion_arterial,
            frecuencia_cardiaca,
            frecuencia_respiratoria,
            temperatura,
            peso,
            talla,
            id_signo,
        ),
    )
    conn.commit()
    conn.close()


def delete_signo_vital(id_signo):
    conn = get_connection()  # Usar get_connection
    c = conn.cursor()
    c.execute("DELETE FROM Signos_Vitales WHERE id_signo = ?", (id_signo,))
    conn.commit()
    conn.close()


def get_signos_vitales_by_paciente(id_paciente, id_usuario):
    """
    Obtiene todos los signos vitales de un paciente específico asociados al usuario logueado.

    Args:
        id_paciente (str): El ID del paciente.
        id_usuario (int): El ID del usuario logueado.

    Returns:
        list[SignoVital]: Una lista de objetos SignoVital.
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        """
        SELECT sv.* 
        FROM Signos_Vitales sv
        JOIN Pacientes p ON sv.id_paciente = p.id_paciente
        WHERE sv.id_paciente = ? AND p.id_usuario = ?
    """,
        (id_paciente, id_usuario),
    )
    rows = c.fetchall()
    conn.close()
    return [SignoVital(*row) for row in rows]


def get_signosvitales_hoy_dao(id_paciente, id_usuario, fecha):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        """
        SELECT sv.* 
        FROM Signos_Vitales sv
        JOIN Pacientes p ON sv.id_paciente = p.id_paciente
        WHERE sv.id_paciente = ? 
        AND sv.fecha = ?
        AND p.id_usuario = ?
        """,
        (id_paciente, fecha, id_usuario),  # Pasamos la fecha como tercer argumento
    )
    row = c.fetchone()  # Obtenemos un solo registro (si existe)
    conn.close()
    return SignoVital(*row) if row else None
