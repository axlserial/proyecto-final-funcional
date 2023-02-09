import services.creators_service as cs
from utils import COLOR_PALETTE
from typing import Callable
import flet as ft

# data de los comics
_total_creators: int = 0
_creators: list[dict[str, any]] = []

# Parametros para las peticiones
_params = {"limit": 10, "offset": 0, "orderBy": "-modified"}


# Order creators by:
_order_by = {
    "none": "No ordenar",
    "firstName": "Primer Nombre",
    "lastName": "Apellido",
}

# Actual forma de ordenar
_actual_order = "none"

# Para obtener los creators
_fetch_func = cs.get_creators(_params)


def creators_view(update_func: Callable):
    # Barra de navegación
    appbar = ft.AppBar(
        title=ft.Text("Creadores"),
        center_title=True,
        bgcolor=COLOR_PALETTE["On-Tertiary"],
        toolbar_height=50,
    )

    def order_creators(e):
        global _actual_order, _params
        _actual_order = str(dp.value)

        set_loading()
        fetch_creators()

    # Dropdown para las formas de ordenar
    dp = ft.Dropdown(
        label="Ordenar por",
        options=list(
            map(
                lambda o: ft.dropdown.Option(text=o[1], key=o[0]),
                _order_by.items(),
            )
        ),
        autofocus=True,
        value="none",
        on_change=order_creators,
    )

    # Contenedor de los creators
    creators_content = ft.Row(
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
                    creators_content,
                    margin=ft.margin.only(top=30),
                ),
            ]
        ),
        margin=ft.margin.only(top=30),
    )

    # Renderiza los creators
    def render_creators():
        # Habilita el dropdown
        dp.disabled = False

        # Limpia contenedor de creators
        creators_content.controls.clear()

        # Genera los creators
        creators_content.controls = list(
            map(
                lambda creator: ft.Container(
                    ft.Card(
                        content=ft.Stack(
                            [
                                ft.Container(
                                    ft.Image(
                                        src=f"{creator['thumbnail']['path']}.{creator['thumbnail']['extension']}",
                                        width=120,
                                        height=120,
                                    ),
                                    alignment=ft.alignment.top_center,
                                    padding=ft.padding.only(top=25, bottom=5),
                                ),
                                ft.Container(
                                    ft.Text(
                                        f"{creator['fullName']}",
                                        text_align="center",
                                    ),
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
                _creators,
            )
        )

        # Añade la paginación (numero de pagina actual)
        pag_text = f"{int(_params['offset'] / _params['limit']) + 1}"
        pag_text += f" de {int(_total_creators / _params['limit']) + 1} páginas"
        creators_content.controls.append(
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
                            disabled=_params["offset"] + _params["limit"] >= _total_creators,
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
        creators_content.controls = [
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

    # Para obtener los creators
    def fetch_creators():
        global _total_creators, _creators, _params

        result = _fetch_func()

        if result != {}:
            _total_creators = result["total"]

            if _actual_order != "none":
                print("Ordenando por", _actual_order)
                _creators = sorted(result["results"], key=lambda c: c[_actual_order])
            else:
                _creators = result["results"]

            render_creators()
        else:
            creators_content.controls = [
                ft.Text("No se han podido obtener los creators, intente de nuevo.")
            ]
            update_func()

    # Para la paginación
    def before_page(e):
        global _params

        if _params["offset"] == 0:
            return

        set_loading()
        _params["offset"] -= _params["limit"]
        fetch_creators()

    def next_page(e):
        global _params, _total_comics

        if _params["offset"] + _params["limit"] >= _total_creators:
            return

        set_loading()
        _params["offset"] += _params["limit"]
        fetch_creators()

    # First fetch
    fetch_creators()

    return [appbar, body]
