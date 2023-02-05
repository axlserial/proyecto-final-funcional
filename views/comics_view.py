from services.comics_service import get_data
import flet as ft


def comics_view(page: ft.page):
    # Obtiene los comics
    comics = get_data('comics')()

    r = ft.Row(wrap=True, expand=True, scroll="always", spacing=10)
    page.add(r)

    if comics == {}:
        r.add(ft.Text('No hay comics'))
    else:
        r.controls = list(
            map(
                lambda comic: ft.Container(
                    ft.Text(comic['title']),
                    width=300,
                    height=300,
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.TEAL_100,
                    border=ft.border.all(1, ft.colors.RED_100),
                    border_radius=ft.border_radius.all(5),
                ), comics))

    page.update()
