from views.principal import principal_view
from views.comics_view import comics_view
from views.personajes_view import characters_view
from views.creators_views import creators_view
from views.historias_view import stories_view
from views.eventos_view import events_view
from views.series_view import series_view


import flet as ft


def main(page: ft.Page):
    # Ventana principal
    page.bgcolor = "#1c1b1e"
    page.title = "Marvel API"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    print("Initial route:", page.route)

    def route_change(e):
        print("Route change:", e.route)
        page.views.clear()

        page.views.append(
            ft.View(
                "/",
                principal_view(page.go),
            )
        )

        if page.route == "/comics":
            page.views.append(
                ft.View(
                    "/comics",
                    comics_view(page.update),
                )
            )

        elif page.route == "/creadores":
            page.views.append(
                ft.View(
                    "/creadores",
                    creators_view(page.update),
                )
            )

        elif page.route == "/personajes":
            page.views.append(
                ft.View(
                    "/personajes",
                    characters_view(page.update, page),
                )
            )

        elif page.route == "/historias":
            page.views.append(
                ft.View(
                    "/historias",
                    stories_view(page.update, page),
                )
            )
            
        elif page.route == "/eventos":
            page.views.append(
                ft.View(
                    "/eventos",
                    events_view(page.update),
                )
            )
            
        elif page.route == "/series":
            page.views.append(
                ft.View(
                    "/series",
                    series_view(page.update),
                )
            )

        #page.update()

    def view_pop(e):
        print("View pop:", e.view)
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go(page.route)


ft.app(target=main, assets_dir="./assets")
