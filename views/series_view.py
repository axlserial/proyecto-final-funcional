# Se agregará en vez de filtrado un ordenamiento
import services.series_service as se
from typing import Callable
import flet as ft
from utils import COLOR_PALETTE

# data de los comics
_total_series: int = 0
_series: list[dict[str, any]] = []

# Parametros para las peticiones
_params = {"limit": 10, "offset": 0, "orderBy": "-modified"}

# Ordenar por:
_format_order = {
    "none": "No ordenar",
    "title": "Título",
    "startYear": "Año de inicio",
}

# Actual forma de filtrar
_actual_order = "none"


# Para obtener los creators
_fetch_func = se.get_series(_params)

def series_view(update_func: Callable):
    
	# Barra de navegación
    appbar = ft.AppBar(
        title=ft.Text("Series"),
        center_title=True,
        bgcolor=COLOR_PALETTE["On-Secondary"],
        toolbar_height=50,
    )

    def order_series(e):
        global _actual_order, _params
        _actual_order = str(dp.value)
        
        
        set_loading()
        fetch_series()
        
	# Dropdown para las formas de ordenar
    dp = ft.Dropdown(
        label="Ordenar por",
        options=list(
            map(
                lambda o: ft.dropdown.Option(text=o[1], key=o[0]),
                _format_order.items(),
            )
        ),
        autofocus=True,
        value="none",
        on_change=order_series,
    )

   
    
	# Contenedor de los creators
    series_content = ft.Row(
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
                    series_content,
                    margin=ft.margin.only(top=30),
                ),
            ]
        ),
        margin=ft.margin.only(top=30),
    )
    
	# Renderiza los creators
    def render_series():
        # Habilita el dropdown
        dp.disabled = False
        
        # Limpia contenedor de creators
        series_content.controls.clear()

        # Genera los creators
        series_content.controls = list(
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
                                        f"{creator['title']}",
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
                    bgcolor=COLOR_PALETTE["On-Primary"],
                ),
                _series,
            )
        )

        # Añade la paginación (numero de pagina actual)
        pag_text = f"{int(_params['offset'] / _params['limit']) + 1}"
        pag_text += f" de {int(_total_series / _params['limit']) + 1} páginas"
        series_content.controls.append(
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
                            disabled=_params["offset"] + _params["limit"] >= _total_series,
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
        series_content.controls = [
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
    
	# Para obtener las series
    def fetch_series():
        global _total_series, _series, _params

        result = _fetch_func()

        if result != {}:
            _total_series = result["total"]

            if _actual_order != "none":
                print("Ordenando por", _actual_order)
                _series = sorted(result["results"], key=lambda c: c[_actual_order])
            else:
                _series = result["results"]

            render_series()
        else:
            series_content.controls = [
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
        fetch_series()

    def next_page(e):
        global _params, _total_comics

        if _params["offset"] + _params["limit"] >= _total_series:
            return

        set_loading()
        _params["offset"] += _params["limit"]
        fetch_series()

    # First fetch
    fetch_series()

    return [appbar, body]
