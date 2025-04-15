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
    get_signos_vitales_by_fecha,
    add_signo_vital,
    update_signo_vital,
)
from services.diagnostico_service import (
    get_diagnosticos_by_consulta,
    add_diagnostico,
    update_diagnostico,
    delete_diagnostico,
)
from services.prescripcion_service import (
    get_prescripciones_by_consulta,
    add_prescripcion,
    update_prescripcion,
    delete_prescripcion,
)
from services.tratamiento_service import (
    get_tratamientos_by_consulta,
    add_tratamiento,
    update_tratamiento,
)
from services.evolucion_service import (
    get_evoluciones_by_consulta,
    add_evolucion,
    update_evolucion,
)
from services.cie_service import get_cie, add_cie


def obtener_historias_clinicas(id_usuario, search_query=""):
    """Obtiene historias clínicas de pacientes con antecedentes médicos, sin duplicados."""

    def normalize_string(s):
        if not s:
            return ""
        return (
            unicodedata.normalize("NFKD", str(s))
            .encode("ASCII", "ignore")
            .decode("ASCII")
            .lower()
        )

    historias = get_historias_clinicas_by_usuario(id_usuario)

    # Filtrar solo pacientes con antecedentes, evitando duplicados por paciente
    historias_unicas = {}
    for h in historias:
        if h.id_paciente in historias_unicas:
            continue
        antecedentes = get_antecedentes_medicos_by_paciente(h.id_paciente, id_usuario)
        if antecedentes:
            historias_unicas[h.id_paciente] = h

    historias_filtradas = list(historias_unicas.values())

    # Filtro por búsqueda si aplica
    if search_query:
        normalized_query = normalize_string(search_query)
        resultados_busqueda = {}
        for h in historias_filtradas:
            paciente = get_paciente(h.id_paciente)
            if not paciente:
                continue

            if normalized_query in normalize_string(
                paciente.nombre
            ) or normalized_query in normalize_string(paciente.apellido):
                # Solo la primera historia por paciente
                if h.id_paciente not in resultados_busqueda:
                    resultados_busqueda[h.id_paciente] = h

        historias_filtradas = list(resultados_busqueda.values())

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


def obtener_signos_por_fecha(id_paciente, id_usuario, fecha):
    return get_signos_vitales_by_fecha(id_paciente, id_usuario, fecha)


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
        (
            signos_vitales["fecha"]
            if "fecha" in signos_vitales and signos_vitales["fecha"]
            else datetime.datetime.now().strftime("%d-%m-%Y")
        ),
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
        (
            diagnostico["fecha"]
            if "fecha" in diagnostico and diagnostico["fecha"]
            else datetime.datetime.now().strftime("%d-%m-%Y")
        ),
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
        (
            prescripcion["fecha"]
            if "fecha" in prescripcion and prescripcion["fecha"]
            else datetime.datetime.now().strftime("%d-%m-%Y")
        ),
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
        (
            tratamiento["fecha"]
            if "fecha" in tratamiento and tratamiento["fecha"]
            else datetime.datetime.now().strftime("%d-%m-%Y")
        ),
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


def guardar_nuevo_cie(codigo: str, descripcion: str) -> str:  # type: ignore
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

        return f"✅ {codigo}"

    except Exception as e:
        print(f"[ERROR] Al guardar CIE: {str(e)}")
        return f"❌ Error al guardar: {str(e)}"


def actualizar_signos_vitales(signos_vitales):
    update_signo_vital(
        signos_vitales["id_signo"],
        signos_vitales["fecha"],
        signos_vitales["presion_arterial"],
        signos_vitales["frecuencia_cardiaca"],
        signos_vitales["frecuencia_respiratoria"],
        signos_vitales["temperatura"],
        signos_vitales["peso"],
        signos_vitales["talla"],
    )


def actualizar_diagnostico(diagnostico):
    print(["Valores de actualizar_diagnostico: ", diagnostico])
    definitivo = 1 if diagnostico["definitivo"] == "Definitivo" else 0
    update_diagnostico(
        diagnostico["id_diagnostico"],
        diagnostico["fecha"],
        diagnostico["diagnostico"],
        diagnostico["cie"],
        definitivo,
    )


def actualizar_prescripcion(prescripcion):
    print(f"\n[Valores que llegan para actualizar prescripcion]: {prescripcion}")
    update_prescripcion(
        prescripcion["id_prescripcion"],
        prescripcion["fecha"],
        prescripcion["medicamento"],
        prescripcion["dosis"],
        prescripcion["indicaciones"],
        prescripcion["firmado_por"],
    )


def actualizar_tratamiento(tratamiento):
    print(f"\n[Valores que llegan para actualizar el tratamiento] {tratamiento}")
    update_tratamiento(
        tratamiento["id_tratamiento"],
        tratamiento["fecha"],
        tratamiento["tratamiento"],
    )


def actualizar_evolucion(evolucion):
    print(f"\n[Valores que llegan para actualizar evolución] {evolucion}")
    update_evolucion(
        evolucion["id_evolucion"],
        evolucion["fecha"],
        evolucion["hora"],
        evolucion["notas"],
    )


def eliminar_diagnostico_crud(id_diagnostico):
    delete_diagnostico(id_diagnostico)


def eliminar_prescripcion(id_prescripcion):
    delete_prescripcion(id_prescripcion)
