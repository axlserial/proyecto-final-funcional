import flet as ft

# Color palette -> https://m3.material.io/theme-builder#/custom
# primary: #6750A4
# secondary: #958DA5
# tertiary: #B58392
# neutral: #939094
# Custom Color 1: #261fa5
# Custom Color 2: #ff7750
# Custom Color 3: #e9d47b

def principal_view(page: ft.Page):
    # Pagina principal
    page.bgcolor = "#1c1b1e"
    page.title = "Marvel information"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # Titulo de la pagina
    title = ft.Container(
        content = ft.Text("Marvel", size=30, color="#ede0de"),
        padding= 20,
        margin= 20,
        alignment=ft.alignment.center,
    )
    page.controls.append(title)

    # Contenido paginas
    secciones = ["Personajes", "Historias", "Series", "Comics", "Creadores", "Eventos"]
    dir_img = map(lambda dir: f"/img/{dir}.png", secciones)
    
    contenido = map(lambda seccion, img: {"seccion": seccion, "img": img}, secciones, dir_img)
    
    # Sección de paginas
    r = ft.Row(wrap=True, expand=True, scroll="always", spacing=13, alignment=ft.MainAxisAlignment.CENTER)
    page.add(r)
    
    r.controls = list(
        map(
            lambda page: ft.Card(
                    ft.Container(
                        ft.Column(  
                            [
                                ft.Text(page["seccion"], size=20, color="#ede0de"), 
                                ft.Image(src= page["img"], width=90, height=90),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        bgcolor="#4f378a",
                        alignment=ft.alignment.center,
                        border_radius=5,
                        ink=True,
                        on_click=lambda e: print(page["seccion"]),
                    ),
                    width=200,
                    height=200
                ), 
                contenido
        )
    )
    
    page.add(
        ft.Container(
            ft.Stack(
                [r]
            )
        )
    )

    page.update()

ft.app(target=principal_view, assets_dir="../assets")