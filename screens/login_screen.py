import flet as ft
import time
from services.usuarios_service import nuevo_usuario

def LoginScreen(page: ft.Page, on_login):
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

    # Mensaje temporal
    mensaje_temporal = ft.Text("", color="red")

    def mostrar_mensaje_temporal(mensaje, color="red"):
        """Muestra un mensaje temporal que desaparece después de 2 segundos"""
        mensaje_temporal.value = mensaje
        mensaje_temporal.color = color
        page.update()  # Actualizar la página para mostrar el mensaje

        # Esperar 1 segundos y luego eliminar el mensaje
        time.sleep(1)
        mensaje_temporal.value = ""
        page.update()

    def toggle_modo(e):
        """Alterna entre el modo Login y Registro"""
        nonlocal modo_registro
        modo_registro = not modo_registro
        page.clean()  # Limpiar la página actual
        page.add(update_view())  # Actualizar la vista con el modo correspondiente
        page.update()  # Asegurar que la página se actualice

    def handle_login(e):
        """Maneja el inicio de sesión"""
        usuario = correo_login_field.value
        password = password_login_field.value
        if usuario and password:
            on_login(usuario, password, mostrar_mensaje_temporal)  # Pasar la función mostrar_mensaje_temporal
        else:
            mostrar_mensaje_temporal("Por favor, complete todos los campos.")

    def handle_register(e):
        """Maneja el registro de un nuevo usuario"""
        if not all([nombre_field.value, apellido_field.value, correo_registro_field.value, password_registro_field.value]):
            mostrar_mensaje_temporal("Todos los campos son obligatorios")
        else:
            resultado = nuevo_usuario(
                nombre_field.value,
                apellido_field.value,
                correo_registro_field.value,
                password_registro_field.value,
            )

            if resultado and resultado.get("status") == "success":
                mostrar_mensaje_temporal("Usuario registrado con éxito", color="green")
                toggle_modo(None)  # Vuelve al modo login
            else:
                mostrar_mensaje_temporal(resultado.get("message", "Error desconocido al registrar el usuario"))

    def update_view():
        """Actualiza la interfaz según el modo actual"""
        nonlocal modo_registro
        if modo_registro:
            # Modo Registro
            return ft.Column(
                [
                    ft.Text("Registrar Nuevo Usuario", size=24, weight=ft.FontWeight.BOLD),
                    nombre_field,
                    apellido_field,
                    correo_registro_field,
                    password_registro_field,
                    ft.ElevatedButton("Crear Usuario", on_click=handle_register),
                    ft.TextButton("Volver al Login", on_click=toggle_modo),
                    mensaje_temporal,  # Mostrar mensaje temporal
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        else:
            # Modo Login
            return ft.Column(
                [
                    ft.Text("Bienvenido", size=24, weight=ft.FontWeight.BOLD),
                    correo_login_field,
                    password_login_field,
                    ft.ElevatedButton("Iniciar sesión", on_click=handle_login),
                    ft.TextButton("Registrarse", on_click=toggle_modo),
                    mensaje_temporal,  # Mostrar mensaje temporal
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )

    # Inicializar la vista con Login
    return ft.Column(
        [
            update_view(),
        ],
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )