import unicodedata
import datetime

from services.historia_clinica_service import (
    get_historias_clinicas_by_usuario,
    update_historia_clinica,
)
from services.paciente_service import get_paciente
from services.antecedente_medico_service import get_antecedentes_medicos_by_paciente
from services.signo_vital_service import (
    get_signos_vitales_by_paciente,
    get_signos_vitales_hoy,
    add_signo_vital,
)
from services.diagnostico_service import get_diagnosticos_by_consulta, add_diagnostico
from services.prescripcion_service import (
    get_prescripciones_by_consulta,
    add_prescripcion,
)
from services.tratamiento_service import get_tratamientos_by_consulta, add_tratamiento
from services.evolucion_service import get_evoluciones_by_consulta
from services.cie_service import get_cie


def obtener_historias_clinicas(id_usuario, search_query=""):
    """Obtiene historias clínicas solo de pacientes con tamizaje completo"""

    def normalize_string(s):
        if not s:
            return ""
        return (
            unicodedata.normalize("NFKD", str(s))
            .encode("ASCII", "ignore")
            .decode("ASCII")
            .lower()
        )

    # Primero obtenemos todas las historias clínicas
    historias = get_historias_clinicas_by_usuario(id_usuario)

    # Filtramos solo las que tienen antecedentes Y signos vitales
    historias_filtradas = []
    for historia in historias:
        antecedentes = get_antecedentes_medicos_by_paciente(
            historia.id_paciente, id_usuario
        )
        signos_vitales = get_signos_vitales_by_paciente(
            historia.id_paciente, id_usuario
        )

        if antecedentes and signos_vitales:  # Solo si tiene ambos
            historias_filtradas.append(historia)

    # Aplicar búsqueda si existe
    if search_query:
        normalized_query = normalize_string(search_query)
        historias_filtradas = [
            h
            for h in historias_filtradas
            if (
                normalized_query in normalize_string(get_paciente(h.id_paciente).nombre)  # type: ignore
            )
            or (
                normalized_query
                in normalize_string(get_paciente(h.id_paciente).apellido)  # type: ignore
            )
        ]

    return historias_filtradas


def actualizar_historia_clinica(
    id_historia, motivo_consulta, enfermedad_actual, id_usuario
):
    """Actualiza una historia clínica existente."""
    return update_historia_clinica(
        id_historia, motivo_consulta, enfermedad_actual, id_usuario
    )


def obtener_diagnosticos_por_consulta(id_paciente, fecha_consulta):
    """Obtiene diagnósticos por paciente y fecha de consulta"""
    return get_diagnosticos_by_consulta(id_paciente, fecha_consulta)


def obtener_prescripciones_por_consulta(id_paciente, fecha_consulta):
    """Obtiene prescripciones por paciente y fecha de consulta"""
    return get_prescripciones_by_consulta(id_paciente, fecha_consulta)


def obtener_tratamientos_por_consulta(id_paciente, fecha_consulta):
    """Obtiene tratamientos por paciente y fecha de consulta"""
    return get_tratamientos_by_consulta(id_paciente, fecha_consulta)


def obtener_evoluciones_por_consulta(id_paciente, fecha_consulta):
    """Obtiene notas de evolución por paciente y fecha de consulta"""
    return get_evoluciones_by_consulta(id_paciente, fecha_consulta)


def obtener_antecedentes_paciente(id_paciente, id_usuario):
    """Obtiene antecedentes médicos de un paciente"""
    return get_antecedentes_medicos_by_paciente(id_paciente, id_usuario)


def obtener_signos_vitales_paciente(id_paciente, id_usuario):
    """Obtiene signos vitales de un paciente"""
    return get_signos_vitales_by_paciente(id_paciente, id_usuario)


def obtener_signos_hoy(id_paciente, id_usuario):
    """Obtiene los signos vitales del paciente de hoy"""
    return get_signos_vitales_hoy(id_paciente, id_usuario)


def obtener_cie(search_query=""):
    """Obtiene códigos CIE con filtro opcional"""
    try:
        resultados = get_cie(search_query)

        # Convertir a formato de diccionario para fácil manejo en la UI
        return [
            {"id": cie.id_cie, "codigo": cie.codigo, "descripcion": cie.descripcion}
            for cie in resultados
        ]

    except Exception as e:
        print(f"Error al obtener CIE: {str(e)}")
        return []


def guardar_signos_vitales(signos_vitales):
    """Guardar signos vitales del paciente"""
    print(f"[evoluciones_crud] signos_vitales: {signos_vitales}")
    add_signo_vital(
        signos_vitales["id_paciente"],
        datetime.datetime.now().strftime("%d-%m-%Y"),
        signos_vitales["presion"],
        signos_vitales["frecuencia_cardiaca"],
        signos_vitales["frecuencia_respiratoria"],
        signos_vitales["temperatura"],
        signos_vitales["peso"],
        signos_vitales["talla"],
    )
    return "Signos vitales guardados"


def guardar_diagnostico(diagnostico):
    """Guardar diagnostico del paciente"""
    print(f"[evoluciones_crud] diagnostico: {diagnostico}")

    add_diagnostico(
        diagnostico["id_paciente"],
        datetime.datetime.now().strftime("%d-%m-%Y"),
        diagnostico["descripcion_cie"],
        diagnostico["codigo_cie"],
        1,  # Definitivo, no se que significa el 1 o cuando no debería ir el 1
        diagnostico["id_usuario"],
    )
    return "Diagnostico guardado"


def guardar_prescripcion(prescripcion):
    """Guardar prescripcion del paciente"""
    print(f"[evoluciones_crud] prescripcion: {prescripcion}")
    add_prescripcion(
        prescripcion["id_paciente"],
        datetime.datetime.now().strftime("%d-%m-%Y"),
        prescripcion["medicamento"],
        prescripcion["dosis"],
        prescripcion["indicaciones"],
        prescripcion["firmado_por"],
        prescripcion["id_usuario"],
    )
    return "Prescripcion guardada"


def guardar_tratamiento(tratamiento):
    """Guardar tratamiento del paciente"""
    print(f"[evoluciones_crud] tratamiento: {tratamiento}")
    add_tratamiento(
        tratamiento["id_paciente"],
        datetime.datetime.now().strftime("%d-%m-%Y"),
        tratamiento["descripcion"],
        tratamiento["id_usuario"],
    )
    return "Tratamiento guardado"
