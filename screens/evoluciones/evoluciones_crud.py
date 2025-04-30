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
from services.evolucion_service import get_evoluciones_by_consulta, add_evolucion
from services.cie_service import get_cie, add_cie


def obtener_historias_clinicas(id_usuario, search_query=""):
    """Obtiene historias clínicas solo de pacientes con tamizaje completo, evitando duplicados"""

    def normalize_string(s):
        if not s:
            return ""
        return (
            unicodedata.normalize("NFKD", str(s))
            .encode("ASCII", "ignore")
            .decode("ASCII")
            .lower()
        )

    # Obtener todas las historias clínicas
    historias = get_historias_clinicas_by_usuario(id_usuario)

    # Diccionario para evitar duplicados por paciente
    historias_unicas = {}

    for historia in historias:
        # Verificar si ya tenemos una historia para este paciente
        if historia.id_paciente in historias_unicas:
            continue

        # Verificar requisitos (antecedentes y signos vitales)
        antecedentes = get_antecedentes_medicos_by_paciente(
            historia.id_paciente, id_usuario
        )
        signos_vitales = get_signos_vitales_by_paciente(
            historia.id_paciente, id_usuario
        )

        if antecedentes and signos_vitales:
            historias_unicas[historia.id_paciente] = historia

    # Convertir a lista
    historias_filtradas = list(historias_unicas.values())

    # Aplicar búsqueda si existe
    if search_query:
        normalized_query = normalize_string(search_query)
        resultados_busqueda = []
        pacientes_vistos = set()

        for h in historias_filtradas:
            paciente = get_paciente(h.id_paciente)
            if not paciente:
                continue

            # Verificar si ya procesamos este paciente
            if paciente.id_paciente in pacientes_vistos:
                continue
            pacientes_vistos.add(paciente.id_paciente)

            # Buscar en nombre y apellido
            if (normalized_query in normalize_string(paciente.nombre)) or (
                normalized_query in normalize_string(paciente.apellido)
            ):
                resultados_busqueda.append(h)

        historias_filtradas = resultados_busqueda

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
    return get_signos_vitales_hoy(
        id_paciente, id_usuario, datetime.datetime.now().strftime("%d-%m-%Y")
    )


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
    definitivo = 1 if diagnostico["definitivo"] == "Definitivo" else 0
    print("               definitivo toma el valor de: ", definitivo)

    add_diagnostico(
        diagnostico["id_paciente"],
        datetime.datetime.now().strftime("%d-%m-%Y"),
        diagnostico["descripcion_cie"],
        diagnostico["codigo_cie"],
        definitivo,
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


def guardar_evolucion(evolucion):
    """Guardar evolucion del paciente"""
    print(f"[evoluciones_crud] evolucion: {evolucion}")
    add_evolucion(
        evolucion["id_paciente"],
        datetime.datetime.now().strftime("%d-%m-%Y"),
        datetime.datetime.now().strftime("%H:%M:%S"),
        evolucion["nota"],
        evolucion["id_usuario"],
    )
    return "Evolucion guardada"

def guardar_nuevo_cie(codigo: str, descripcion: str) -> str:
    """
    Guarda un nuevo código CIE en la base de datos local.
    
    Args:
        codigo (str): Código CIE (ej: "E11.9").
        descripcion (str): Descripción del diagnóstico.
    
    Returns:
        str: Mensaje de confirmación o error.
    """
    try:
        from services.cie_service import add_cie
        
        # Validación básica
        if not codigo or not descripcion:
            return "❌ Código y descripción son obligatorios"
        
        # Guardar usando la función existente en cie_service
        add_cie(codigo, descripcion)
    
    except Exception as e:
        print(f"[ERROR] Al guardar CIE: {str(e)}")
        return f"❌ Error al guardar: {str(e)}"