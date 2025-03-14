import flet as ft
from services.usuarios_service import nuevo_usuario

def LoginScreen(page, on_login):
    """Pantalla combinada de Login y Registro en la misma interfaz"""

    # Variable de estado para alternar entre login y registro
    modo_registro = False  

    # Campos de login
    correo_login_field = ft.TextField(label="Correo")
    password_login_field = ft.TextField(label="Contraseña", password=True)

    # Campos de registro
    nombre_field = ft.TextField(label="Nombre")
    apellido_field = ft.TextField(label="Apellido")
    correo_registro_field = ft.TextField(label="Correo")
    password_registro_field = ft.TextField(label="Contraseña", password=True)

    mensaje_texto = ft.Text("")  # Para mostrar mensajes de error o éxito

    def toggle_modo(e):
        """Alterna entre el modo Login y Registro"""
        nonlocal modo_registro
        modo_registro = not modo_registro
        update_view()

    def handle_login(e):
        """Maneja el inicio de sesión"""
        usuario = correo_login_field.value
        password = password_login_field.value
        on_login(usuario, password)

    def handle_register(e):
        """Maneja el registro de un nuevo usuario"""
        if not all([nombre_field.value, apellido_field.value, correo_registro_field.value, password_registro_field.value]):
            mensaje_texto.value = "Todos los campos son obligatorios"
            mensaje_texto.color = "red"
        else:
            resultado = nuevo_usuario(
                nombre_field.value,
                apellido_field.value,
                correo_registro_field.value,
                password_registro_field.value,
            )

            if resultado["status"] == "success":
                mensaje_texto.value = "Usuario registrado con éxito"
                mensaje_texto.color = "green"
                toggle_modo(None)  # Vuelve al modo login
            else:
                mensaje_texto.value = resultado["message"]
                mensaje_texto.color = "red"

        update_view()

    def update_view():
        """Actualiza la interfaz según el modo actual"""
        page.controls.clear()
        if modo_registro:
            # Modo Registro
            page.add(
                ft.Text("Registrar Nuevo Usuario", size=24, weight=ft.FontWeight.BOLD),
                nombre_field,
                apellido_field,
                correo_registro_field,
                password_registro_field,
                mensaje_texto,
                ft.ElevatedButton("Crear Usuario", on_click=handle_register),
                ft.TextButton("Volver al Login", on_click=toggle_modo),
            )
        else:
            # Modo Login
            page.add(
                ft.Text("Bienvenido", size=24, weight=ft.FontWeight.BOLD),
                correo_login_field,
                password_login_field,
                mensaje_texto,
                ft.ElevatedButton("Iniciar sesión", on_click=handle_login),
                ft.TextButton("Registrarse", on_click=toggle_modo),
            )
        page.update()

    # Inicializar la vista con Login
    update_view()
