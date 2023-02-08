import services.comics_service as cs
from utils import COLOR_PALETTE
from typing import Callable
import flet as ft

# data de los comics
_total_comics: int = 0
_comics: list[dict[str, any]] = []

# Para la paginación
_params = {"limit": 10, "offset": 0}


# Filtro de comics por formato
format_filters = [
    "none",
    "comic",
    "magazine",
    "trade paperback",
    "hardcover",
    "digest",
    "graphic novel",
    "digital comic",
    "infinite comic",
]

# Filtro por formato de comic
_actual_format_filter = format_filters[0]

# Para obtener los comics
_fetch_func = cs.get_comics(_params)


def comics_view(update_func: Callable):
    # Barra de navegación
    appbar = ft.AppBar(
        title=ft.Text("Comics"),
        center_title=True,
        bgcolor=COLOR_PALETTE["On-Tertiary"],
        toolbar_height=50,
    )

    def filter_comics(e):
        global _actual_format_filter, _params
        _actual_format_filter = str(dp.value)
        _params["offset"] = 0

        set_loading()
        fetch_comics()

    # Dropdown de filtros
    dp = ft.Dropdown(
        label="Filtrar por",
        options=list(
            map(
                lambda f: ft.dropdown.Option(text=f.capitalize(), key=f),
                format_filters,
            )
        ),
        autofocus=True,
        value=format_filters[0],
        on_change=filter_comics,
    )

    # Contenedor de los comics
    comics_content = ft.Row(
        wrap=True,
        expand=True,
        scroll="always",
        spacing=10,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # Cuerpo de la página
    body = ft.Container(
        ft.Column(
            [
                ft.Row(
                    [dp],
                    alignment="center",
                ),
                ft.Container(
                    comics_content,
                    margin=ft.margin.only(top=30),
                ),
            ]
        ),
        margin=ft.margin.only(top=30),
    )

    # Renderiza los comics
    def render_comics():
        # Habilita el dropdown
        dp.disabled = False

        # Limpia contenedor de comics
        comics_content.controls.clear()

        # Genera los comics
        comics_content.controls = list(
            map(
                lambda comic: ft.Container(
                    ft.Card(
                        content=ft.Stack(
                            [
                                ft.Container(
                                    ft.Image(
                                        src=f"{comic['thumbnail']['path']}.{comic['thumbnail']['extension']}",
                                        width=120,
                                        height=120,
                                    ),
                                    alignment=ft.alignment.top_center,
                                    padding=ft.padding.only(top=25, bottom=5),
                                ),
                                ft.Container(
                                    ft.Text(comic["title"], text_align="center"),
                                    alignment=ft.alignment.bottom_center,
                                    padding=ft.padding.only(left=5, right=5, bottom=15),
                                ),
                            ],
                        ),
                    ),
                    width=230,
                    height=230,
                    bgcolor=COLOR_PALETTE["On-Error"],
                ),
                _comics,
            )
        )

        # Añade la paginación (numero de pagina actual)
        pag_text = f"{int(_params['offset'] / _params['limit']) + 1}"
        pag_text += f" de {int(_total_comics / _params['limit']) + 1} páginas"
        comics_content.controls.append(
            ft.Container(
                ft.Row(
                    [
                        ft.IconButton(
                            icon=ft.icons.ARROW_BACK,
                            disabled=_params["offset"] == 0,
                            on_click=before_page,
                        ),
                        ft.Text(pag_text),
                        ft.IconButton(
                            icon=ft.icons.ARROW_FORWARD,
                            disabled=_params["offset"] + _params["limit"] >= _total_comics,
                            on_click=next_page,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                padding=ft.padding.only(top=20),
            )
        )

        update_func()

    # render loading indicator
    def set_loading():
        # Deshabilita el dropdown
        dp.disabled = True

        # Muestra el indicador de carga
        comics_content.controls = [
            ft.Container(
                ft.Column(
                    [ft.ProgressRing(), ft.Text("Cargando...")],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                alignment=ft.alignment.center,
                margin=ft.margin.only(top=50),
            )
        ]
        update_func()

    # Para obtener los comics
    def fetch_comics():
        global _total_comics, _comics, _params

        # Si el filtro es none, se elimina el parametro de la consulta
        if "format" in _params:
            del _params["format"]

        # Si el filtro es distinto de none, se agrega el parametro de la consulta
        if _actual_format_filter != "none":
            _params["format"] = _actual_format_filter

        result = _fetch_func()

        if result != {}:
            _total_comics = result["total"]
            _comics = result["results"]
            render_comics()
        else:
            comics_content.controls = [
                ft.Text("No se han podido obtener los comics, intente de nuevo.")
            ]
            update_func()

    # Para la paginación
    def before_page(e):
        global _params

        if _params["offset"] == 0:
            return

        set_loading()
        _params["offset"] -= _params["limit"]
        fetch_comics()

    def next_page(e):
        global _params, _total_comics

        if _params["offset"] + _params["limit"] >= _total_comics:
            return

        set_loading()
        _params["offset"] += _params["limit"]
        fetch_comics()

    # First fetch
    fetch_comics()

    return [appbar, body]
