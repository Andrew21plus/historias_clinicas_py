import flet as ft
from datetime import datetime, timedelta
from .certificado_crud import buscar_pacientes, obtener_diagnosticos_paciente
from .certificado_ui import crear_buscador_pacientes, crear_formulario_certificado
from .pdf_generator_certificados import generar_pdf_certificado

def CertificadoScreen(page: ft.Page, id_usuario: int):
    # Estado
    paciente_seleccionado = None
    diagnosticos_seleccionados = []
    diagnosticos_disponibles = []
    
    # Alertas
    alert_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Notificación"),
        content=ft.Text(""),
        actions=[ft.TextButton("OK", on_click=lambda e: cerrar_alerta())]
    )
    
    # DatePicker para seleccionar fecha de consulta
    fecha_consulta_picker = ft.DatePicker(
        first_date=datetime.now() - timedelta(days=365*2),
        last_date=datetime.now(),
        on_change=lambda e: actualizar_diagnosticos()
    )
    
    # Añadir el DatePicker a los overlays de la página
    page.overlay.append(fecha_consulta_picker)
    
    def cerrar_alerta():
        alert_dialog.open = False
        page.update()
    
    def show_alert(message):
        alert_dialog.content.value = message
        alert_dialog.open = True
        page.update()
    
    def actualizar_cie():
        # Actualizar campo CIE con todos los códigos seleccionados
        cies = [d.cie for d in diagnosticos_seleccionados]
        formulario["cie"].value = "\n".join(cies)
        page.update()
    
    def on_diagnostico_change(diagnostico, checkbox):
        if checkbox.value:
            diagnosticos_seleccionados.append(diagnostico)
        else:
            diagnosticos_seleccionados.remove(diagnostico)
        actualizar_cie()
    
    def abrir_selector_fecha(e):
        fecha_consulta_picker.open = True
        page.update()
    
    def actualizar_diagnosticos():
        if paciente_seleccionado:
            fecha_seleccionada = fecha_consulta_picker.value
            if isinstance(fecha_seleccionada, datetime):
                fecha_seleccionada = fecha_seleccionada.date()

            fecha_str = fecha_seleccionada.strftime("%d-%m-%Y")


            diagnosticos = obtener_diagnosticos_paciente(
                paciente_seleccionado.id_paciente, 
                fecha_str
            )
            #print("Diagnosticos para el paciente: ", paciente_seleccionado.id_paciente , "en la fecha: ", fecha_str , "= " , diagnosticos)
            diagnosticos_disponibles = diagnosticos
            diagnosticos_seleccionados.clear()
            
            # Limpiar contenedor y agregar checkboxes para cada diagnóstico
            formulario["diagnostico_container"].controls.clear()
            for d in diagnosticos:
                checkbox = ft.Checkbox(
                    label=f"{d.diagnostico} ({d.cie})",
                    value=False,
                    on_change=lambda e, d=d: on_diagnostico_change(d, e.control)
                )
                formulario["diagnostico_container"].controls.append(checkbox)
            
            formulario["fecha_consulta"].value = fecha_seleccionada.strftime("%d/%m/%Y")
            formulario["cie"].value = ""
            page.update()
    
    def on_paciente_search(e):
        query = buscador["search_field"].value
        resultados = buscar_pacientes(id_usuario, query)
        
        buscador["pacientes_list"].controls.clear()
        for paciente in resultados:
            buscador["pacientes_list"].controls.append(
                ft.ListTile(
                    title=ft.Text(f"{paciente.nombre} {paciente.apellido}"),
                    on_click=lambda e, p=paciente: on_paciente_select(p)
                )
            )
        page.update()
    
    def on_paciente_select(paciente):
        nonlocal paciente_seleccionado
        paciente_seleccionado = paciente
        buscador["search_field"].value = f"{paciente.nombre} {paciente.apellido}"
        buscador["pacientes_list"].controls.clear()
        
        # Configurar el botón de fecha
        formulario["fecha_consulta_button"].on_click = abrir_selector_fecha
        formulario["fecha_consulta_button"].disabled = False
        
        # Establecer fecha predeterminada (hoy)
        fecha_consulta_picker.value = datetime.now().date()
        formulario["fecha_consulta"].value = fecha_consulta_picker.value.strftime("%d/%m/%Y")
        
        # Limpiar selecciones anteriores
        diagnosticos_seleccionados.clear()
        formulario["diagnostico_container"].controls.clear()
        formulario["cie"].value = ""
        
        # Mostrar formulario
        formulario["form"].visible = True
        btn_generar_pdf.disabled = False
        page.update()
    
    def generar_pdf(e):
        if not paciente_seleccionado:
            show_alert("Seleccione un paciente primero")
            return
            
        if not diagnosticos_seleccionados:
            show_alert("Seleccione al menos un diagnóstico")
            return
            
        if not formulario["indicaciones"].value:
            show_alert("Ingrese las indicaciones médicas")
            return
            
        data = {
            "paciente": paciente_seleccionado,
            "diagnosticos": [f"{d.diagnostico} ({d.cie})" for d in diagnosticos_seleccionados],
            "cies": [d.cie for d in diagnosticos_seleccionados],
            "contingencia": formulario["contingencia"].value,
            "indicaciones": formulario["indicaciones"].value,
            "dias_reposo": formulario["dias_reposo"].value,
            "fecha_emision": datetime.now().strftime("%d/%m/%Y"),
            "fecha_consulta": formulario["fecha_consulta"].value
        }
        
        try:
            pdf_path = generar_pdf_certificado(data)
            show_alert(f"Certificado generado exitosamente\nGuardado en: {pdf_path}")
        except Exception as e:
            show_alert(f"Error al generar PDF: {str(e)}")
    
    # Componentes UI
    buscador = crear_buscador_pacientes(on_paciente_search, on_paciente_select)
    formulario = crear_formulario_certificado()
    formulario["form"].visible = False
    
    # PDF Button
    btn_generar_pdf = ft.ElevatedButton(
        "Generar Certificado PDF",
        icon=ft.icons.PICTURE_AS_PDF,
        on_click=generar_pdf,
        disabled=True
    )
    
    # Contenedor principal
    content = ft.Column(
        [
            ft.Text("Certificados Médicos", size=24, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            buscador["container"],
            formulario["form"],
            ft.Row([btn_generar_pdf], alignment=ft.MainAxisAlignment.CENTER),
            alert_dialog
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True
    )
    
    return ft.Container(
        content=content,
        padding=20,
        expand=True
    )