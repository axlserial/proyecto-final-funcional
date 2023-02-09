import services.eventos_service as es
from typing import Callable
import flet as ft


# Respuesta de la API
result = es.get_events()

# Paginación
paginacion: dict[str,int] = {'limit': 0, 'offset': 0}

def events_view(update_func: Callable):

    # Contenedor de los eventos
    events_content = ft.Row(
        wrap=True,
        expand=True,
        scroll="always",
        spacing=10,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # Cuerpo de la página
    body = ft.Container(events_content,
                        margin=ft.margin.only(top=30),
                        width=1280,
                        height=720)
    
    # Barra de navegación
    appbar = ft.AppBar(
        title=ft.Text("Comics"),
        center_title=True,
        bgcolor=ft.colors.SURFACE_VARIANT,
    )
    
    
    return [appbar, body]