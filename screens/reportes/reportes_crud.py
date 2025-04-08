from datetime import datetime, timedelta
from collections import defaultdict
from services.diagnostico_service import get_diagnosticos
from services.paciente_service import get_pacientes_by_id_usuario
from services.evolucion_service import get_evoluciones_by_usuario
from services.prescripcion_service import get_prescripciones_by_usuario
from services.cie_service import get_cie_by_id_service

def parse_fecha(fecha_str):
    """Convierte string de fecha (dd-mm-yyyy) a objeto datetime"""
    if isinstance(fecha_str, datetime):
        return fecha_str
    try:
        return datetime.strptime(fecha_str, '%d-%m-%Y')
    except (ValueError, TypeError, AttributeError):
        try:
            return datetime.strptime(fecha_str, '%Y-%m-%d')
        except:
            return None

def obtener_diagnosticos_frecuentes(id_usuario, periodo=None, fecha_inicio=None, fecha_fin=None, limite=10):
    """Obtiene diagnósticos más frecuentes con filtros de fecha"""
    diagnosticos = get_diagnosticos()
    
    conteo_cie = defaultdict(int)
    for d in diagnosticos:
        if d.id_usuario == id_usuario:
            fecha = parse_fecha(getattr(d, 'fecha', None))
            if fecha:
                # Verificar si cumple con los filtros de fecha
                fecha_valida = True
                
                # Filtrar por periodo si está especificado (mantenemos compatibilidad)
                if periodo and fecha.strftime('%Y-%m') != periodo:
                    fecha_valida = False
                
                # Filtrar por rango de fechas si está especificado
                if fecha_inicio and fecha.date() < fecha_inicio:
                    fecha_valida = False
                
                if fecha_fin and fecha.date() > fecha_fin:
                    fecha_valida = False
                
                if fecha_valida:
                    conteo_cie[d.cie] += 1
    
    resultados = sorted(conteo_cie.items(), key=lambda x: x[1], reverse=True)[:limite]
    return [(codigo, obtener_descripcion_cie(codigo), count) for codigo, count in resultados]

def obtener_distribucion_sexo(id_usuario):
    """Distribución por sexo con manejo seguro de fechas"""
    pacientes = {p.id_paciente: p for p in get_pacientes_by_id_usuario(id_usuario)}
    diagnosticos = get_diagnosticos()
    
    distribucion = {'M': 0, 'F': 0, 'O': 0}
    for d in diagnosticos:
        if d.id_usuario == id_usuario and d.id_paciente in pacientes:
            sexo = pacientes[d.id_paciente].sexo
            distribucion[sexo] += 1
    
    return [(sexo, count) for sexo, count in distribucion.items()]

def obtener_tendencias_temporales(id_usuario, codigo_cie=None):
    """Tendencias temporales con cálculo de variación porcentual"""
    diagnosticos = get_diagnosticos()
    
    tendencias = defaultdict(int)
    for d in diagnosticos:
        if d.id_usuario == id_usuario and (codigo_cie is None or d.cie == codigo_cie):
            fecha = parse_fecha(getattr(d, 'fecha', None))
            if fecha:
                tendencias[fecha.strftime('%Y-%m')] += 1
    
    # Completar con los últimos 12 meses si no hay datos
    if not tendencias:
        last_month = datetime.now().replace(day=1) - timedelta(days=1)
        for i in range(12):
            month = last_month - timedelta(days=30*i)
            tendencias[month.strftime('%Y-%m')] = 0
    
    datos = completar_meses_faltantes(sorted(tendencias.items()))
    
    # Calcular variaciones porcentuales
    variaciones = []
    for i in range(len(datos)):
        if i == 0:
            variaciones.append(0)
        else:
            anterior = datos[i-1][1]
            actual = datos[i][1]
            cambio = ((actual - anterior) / anterior * 100) if anterior != 0 else 0
            variaciones.append(cambio)
    
    return datos, variaciones

def obtener_pacientes_diagnosticados_por_periodo(id_usuario, periodo='month'):
    """Obtiene cantidad de pacientes únicos diagnosticados por período"""
    pacientes = {p.id_paciente: p for p in get_pacientes_by_id_usuario(id_usuario)}
    diagnosticos = get_diagnosticos()
    
    pacientes_por_periodo = defaultdict(set)
    
    for d in diagnosticos:
        if d.id_usuario == id_usuario and d.id_paciente in pacientes:
            fecha = parse_fecha(getattr(d, 'fecha', None))
            if fecha:
                key = format_periodo(fecha, periodo)
                pacientes_por_periodo[key].add(d.id_paciente)
    
    resultados = [(periodo, len(pacientes)) for periodo, pacientes in pacientes_por_periodo.items()]
    return completar_periodos_faltantes(sorted(resultados), periodo)

def obtener_prescripciones_frecuentes(id_usuario, limite=12):
    """Prescripciones frecuentes sin dependencia de fechas"""
    prescripciones = get_prescripciones_by_usuario(id_usuario)
    conteo = defaultdict(int)
    for p in prescripciones:
        conteo[p.medicamento] += 1
    return sorted(conteo.items(), key=lambda x: x[1], reverse=True)[:limite]

def obtener_periodos_disponibles(id_usuario):
    """Obtiene períodos disponibles dinámicamente"""
    diagnosticos = get_diagnosticos()
    periodos = set()
    for d in diagnosticos:
        if d.id_usuario == id_usuario:
            fecha = parse_fecha(getattr(d, 'fecha', None))
            if fecha:
                periodos.add(fecha.strftime('%Y-%m'))
    return sorted(periodos, reverse=True)

def obtener_cie_disponibles(id_usuario):
    """Obtiene códigos CIE usados dinámicamente"""
    diagnosticos = get_diagnosticos()
    return sorted({d.cie for d in diagnosticos if d.id_usuario == id_usuario and d.cie})

# Funciones auxiliares
def format_periodo(fecha, periodo):
    if periodo == 'month':
        return fecha.strftime('%Y-%m')
    elif periodo == 'week':
        return fecha.strftime('%Y-%W')
    else:  # day
        return fecha.strftime('%Y-%m-%d')

def completar_periodos_faltantes(datos, periodo):
    if not datos:
        return datos
    
    try:
        if periodo == 'month':
            dates = [datetime.strptime(d[0], '%Y-%m') for d in datos]
            min_date, max_date = min(dates), max(dates)
            current = min_date
            while current <= max_date:
                key = current.strftime('%Y-%m')
                if not any(d[0] == key for d in datos):
                    datos.append((key, 0))
                if current.month == 12:
                    current = current.replace(year=current.year+1, month=1)
                else:
                    current = current.replace(month=current.month+1)
        
        elif periodo == 'week':
            dates = [datetime.strptime(d[0]+'-1', '%Y-%W-%w') for d in datos]
            min_date, max_date = min(dates), max(dates)
            current = min_date
            while current <= max_date:
                key = current.strftime('%Y-%W')
                if not any(d[0] == key for d in datos):
                    datos.append((key, 0))
                current += timedelta(weeks=1)
        
        else:  # day
            dates = [datetime.strptime(d[0], '%Y-%m-%d') for d in datos]
            min_date, max_date = min(dates), max(dates)
            current = min_date
            while current <= max_date:
                key = current.strftime('%Y-%m-%d')
                if not any(d[0] == key for d in datos):
                    datos.append((key, 0))
                current += timedelta(days=1)
        
        return sorted(datos, key=lambda x: x[0])
    
    except ValueError:
        return datos

def completar_meses_faltantes(datos):
    if not datos:
        return datos
    
    try:
        dates = [datetime.strptime(d[0], '%Y-%m') for d in datos]
        min_date, max_date = min(dates), max(dates)
        current = min_date
        while current <= max_date:
            key = current.strftime('%Y-%m')
            if not any(d[0] == key for d in datos):
                datos.append((key, 0))
            if current.month == 12:
                current = current.replace(year=current.year+1, month=1)
            else:
                current = current.replace(month=current.month+1)
        
        return sorted(datos, key=lambda x: x[0])
    
    except ValueError:
        return datos

def obtener_descripcion_cie(codigo_cie):
    """Obtiene la descripción desde la base de datos"""
    cie = get_cie_by_id_service(codigo_cie)
    if cie and hasattr(cie, 'descripcion'):
        return cie.descripcion
    return f"Código {codigo_cie}"