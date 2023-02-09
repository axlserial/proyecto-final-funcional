import flet as ft
from utils import COLOR_PALETTE


def principal_view(change_page_func):

    # Titulo de la pagina
    title = ft.Container(
        content=ft.Text("Marvel", size=30, color=COLOR_PALETTE["On-Background"]),
        padding=20,
        margin=20,
        alignment=ft.alignment.center,
    )

    # Contenido paginas
    secciones = [
        "Personajes", "Historias", "Series", "Comics", "Creadores", "Eventos"
    ]
    dir_img = map(lambda dir: f"/img/{dir}.png", secciones)

    contenido = map(lambda seccion, img: {
        "seccion": seccion,
        "img": img
    }, secciones, dir_img)

    # Sección de paginas
    r = ft.Row(wrap=True,
               expand=True,
               scroll="always",
               spacing=13,
               alignment=ft.MainAxisAlignment.CENTER)

    r.controls = list(
        map(
            lambda page: ft.Card(ft.Container(
                ft.Column(
                    [
                        ft.Text(page["seccion"], size=20, color=COLOR_PALETTE["On-Background"]),
                        ft.Image(src=page["img"], width=90, height=90),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                bgcolor=COLOR_PALETTE["Primary-Container"],
                alignment=ft.alignment.center,
                border_radius=5,
                ink=True,
                on_click=lambda e: change_page_func(
                    f'/{page["seccion"].lower()}'),
            ),
                                 width=200,
                                 height=200), contenido))

    return [title, ft.Container(r, alignment=ft.alignment.center)]