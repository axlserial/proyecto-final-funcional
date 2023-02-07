from views.principal import principal_view
from views.comics_view import comics_view
from views.personajes import characters_view
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

        page.views.append(ft.View(
            "/",
            principal_view(page.go),
        ))

        if page.route == "/comics":
            page.views.append(ft.View(
                "/comics",
                comics_view(page.update),
            ))

        elif page.route == "/personajes":
            page.views.append(ft.View(
                "/personajes",
                characters_view(page.update,page),
            ))

        page.update()

    def view_pop(e):
        print("View pop:", e.view)
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go(page.route)


ft.app(target=main, assets_dir="./assets")