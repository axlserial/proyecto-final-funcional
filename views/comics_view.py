import services.comics_service as cs
from typing import Callable
from enum import Enum
import flet as ft

# data de los comics
_total_comics: int = 0
_comics: list[dict[str, any]] = []

# Para la paginación
_pagination = {'limit': 10, 'offset': 0}


# Filtro de comics por formato
class FormatFilter(Enum):
    NONE = 'none'
    COMIC = 'comic'
    MAGAZINE = 'magazine'
    TRADE_PAPERBACK = 'trade paperback'
    HARDCOVER = 'hardcover'
    DIGEST = 'digest'
    GRAPHIC_NOVEL = 'graphic novel'
    DIGITAL_COMIC = 'digital comic'
    INFINITE_COMIC = 'infinite comic'


# Filtro por formato de comic
_actual_format_filter = FormatFilter.NONE.value

# Para obtener los comics
_fetch_func = cs.get_comics(_pagination)


def comics_view(update_func: Callable):
    # Contenedor de los comics
    comics_content = ft.Row(
        wrap=True,
        expand=True,
        scroll="always",
        spacing=10,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # Cuerpo de la página
    body = ft.Container(comics_content,
                        margin=ft.margin.only(top=30),
                        width=1280,
                        height=720)

    def filter_comics(e):
        global _actual_format_filter
        _actual_format_filter = e.control.value

        set_loading()
        fetch_comics()

    # Barra de navegación
    appbar = ft.AppBar(
        title=ft.Text("Comics"),
        center_title=True,
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[
            ft.Container(ft.PopupMenuButton(items=[
                ft.PopupMenuItem(content=ft.RadioGroup(content=ft.Column(
                    list(
                        map(
                            lambda f: ft.Radio(value=f.value,
                                               label=f.value.capitalize()),
                            FormatFilter))),
                                                       on_change=filter_comics)
                                 )
            ],
                                            tooltip="Filtros",
                                            icon=ft.icons.FILTER_LIST),
                         padding=ft.padding.all(5),
                         alignment=ft.alignment.center,
                         margin=ft.margin.only(right=5)),
        ],
    )

    # Renderiza los comics
    def render_comics():
        # Limpia contenedor de comics
        comics_content.controls.clear()

        # Genera los comics
        comics_content.controls = list(
            map(
                lambda comic: ft.Container(ft.Card(content=ft.Stack([
                    ft.Container(
                        ft.Image(
                            src=
                            f"{comic['thumbnail']['path']}.{comic['thumbnail']['extension']}",
                            width=120,
                            height=120,
                        ),
                        alignment=ft.alignment.top_center,
                        padding=ft.padding.only(top=25, bottom=5),
                    ),
                    ft.Container(
                        ft.Text(comic['title'], text_align="center"),
                        alignment=ft.alignment.bottom_center,
                        padding=ft.padding.only(left=5, right=5, bottom=15),
                    )
                ], ), ),
                                           width=230,
                                           height=230,
                                           bgcolor="#4f378a",
                                           ink=True,
                                           on_click=lambda e: print(comic[
                                               'id'])), _comics))

        # Añade la paginación
        pag_text = f"{_pagination['offset'] + 1} - {_pagination['offset'] + _pagination['limit']} de {_total_comics}"
        comics_content.controls.append(
            ft.Container(ft.Row(
                [
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        disabled=_pagination['offset'] == 0,
                        on_click=before_page,
                    ),
                    ft.Text(pag_text),
                    ft.IconButton(
                        icon=ft.icons.ARROW_FORWARD,
                        disabled=_pagination['offset'] + _pagination['limit']
                        >= _total_comics,
                        on_click=next_page,
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
                         padding=ft.padding.only(top=20)))

        update_func()

    # render loading indicator
    def set_loading():
        # Muestra el indicador de carga
        comics_content.controls = [
            ft.Container(ft.Column(
                [ft.ProgressRing(), ft.Text("Cargando...")],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
                         alignment=ft.alignment.center)
        ]
        update_func()

    # Para obtener los comics
    def fetch_comics():
        global _total_comics, _comics

        result = _fetch_func()

        if result != {}:
            _total_comics = result['total']
            _comics = result['results']
            render_comics()
        else:
            body.controls = [
                ft.Text(
                    'No se han podido obtener los comics, intente de nuevo.')
            ]
            update_func()

    # Para la paginación
    def before_page(e):
        global _pagination

        if _pagination['offset'] == 0:
            return

        set_loading()
        _pagination['offset'] -= _pagination['limit']
        fetch_comics()

    def next_page(e):
        global _pagination, _total_comics

        if _pagination['offset'] + _pagination['limit'] >= _total_comics:
            return

        set_loading()
        _pagination['offset'] += _pagination['limit']
        fetch_comics()

    # First fetch
    fetch_comics()

    return [appbar, body]
