import flet as ft
import services.personajes_service as PJ
from typing import Callable
from utils import COLOR_PALETTE

def characters_view(update_func: Callable, page : ft.Page):
    #Funcion de control de paginas
    def next_page(e):
        r.controls.clear()
        if int(txt_number.value) < int(totalPages.value) :
            txt_number.value = int(txt_number.value) +1
            cards(page.client_storage.get("objectsPage"))
        else:
            txt_number.value = 1
            cards(page.client_storage.get("objectsPage"))

    def before_page(e):
        r.controls.clear()
        if int(txt_number.value) == 1:
            txt_number.value = int(totalPages.value)
            cards(page.client_storage.get("objectsPage"))
        
        else:
            txt_number.value = int(txt_number.value) - 1
            cards(page.client_storage.get("objectsPage"))

    def cards(cardsPage):
        if cardsPage != []:
            if int(txt_number.value) == int(totalPages.value):
                [
                    r.controls.append(
                        ft.Card(
                            ft.Container(
                                ft.Column(
                                    [
                                        ft.Text(cardsPage[i-1]["nombre"],color = COLOR_PALETTE["On-Primary"], text_align = "center" , selectable=False , ),
                                        ft.Image(
                                            src=cardsPage[i-1]['imagen'],
                                            width=100,
                                            height=100,
                                        ),
                                        ft.Text(cardsPage[i-1]["id"],color = COLOR_PALETTE["On-Primary"],selectable=False,text_align = "center", ), 
                                        ft.Text(cardsPage[i-1]["descripcion"][:23]+"...",color = "#381e72",selectable=False,text_align = "center",),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                                ),
                                bgcolor= "#cfbcff",
                                border= ft.border.all(1,  "#C4ACFF"),
                                border_radius= ft.border_radius.all(5),
                                alignment = ft.alignment.center,
                            ),
                            width=200,
                            height=200,
                        )
                    )

                    for i in range(((-9)+(int(txt_number.value)*9))+1, (len(cardsPage))+1)
                ]

            else:
                [
                    r.controls.append(
                        ft.Card(
                            ft.Container(
                                ft.Column(
                                    [
                                        ft.Text(cardsPage[i-1]["nombre"],color = COLOR_PALETTE["On-Primary"], text_align = "center" , selectable=False , ),
                                        ft.Image(
                                            src=cardsPage[i-1]['imagen'],
                                            width=100,
                                            height=100,
                                        ),
                                        ft.Text(cardsPage[i-1]["id"],color = COLOR_PALETTE["On-Primary"],selectable=False,text_align = "center" , ), 
                                        ft.Text(cardsPage[i-1]["descripcion"][:23]+"...",color = COLOR_PALETTE["On-Primary"],selectable=False,text_align = "center", ),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                                ),
                                bgcolor= "#cfbcff",
                                border= ft.border.all(1, "#C4ACFF"),
                                border_radius= ft.border_radius.all(5),
                                alignment = ft.alignment.center,
                            ),
                            width=200,
                            height=200,
                        )
                    )

                    for i in range(((-9)+(int(txt_number.value)*9))+1 ,(int(txt_number.value)*9)+1)
                ]

        else:
            r.controls.append(
                ft.Card(
                    ft.Container(
                        ft.Column(
                            [
                                ft.Text("No hay personajes", text_align = "center" ,color = "#381e72", selectable=False ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                        ),
                        bgcolor= COLOR_PALETTE["On-Error"],
                        border= ft.border.all(1,"#FCA196"),
                        border_radius= ft.border_radius.all(5),
                        alignment = ft.alignment.center,
                    ),
                    width=200,
                    height=200,
                ),
            ),

        update_func()

    def dropdown_changed(e):
        r.controls.clear()
        txt_number.value = 1
        update_func()

        if dd.value == "ALL The Characters":
            page.client_storage.set("objectsPage", requestF.copy())
            totalPages.value = int(len(page.client_storage.get("objectsPage")) / 9)
        elif dd.value == "Characters with comics":
            page.client_storage.set("objectsPage", [data for data in requestF if data['comics'] != []])
            if len(page.client_storage.get("objectsPage")) % 9 == 0:
                totalPages.value = int(len(page.client_storage.get("objectsPage")) / 9)
            else :
                totalPages.value = int(len(page.client_storage.get("objectsPage")) / 9) + 1
        elif dd.value == "The *Avengers* comics":
            unique_sweets = []
            [unique_sweets.append(sweet) for sweet in [data for data in requestF for comic in data['comics'] if 'Avengers' in comic] if sweet not in unique_sweets]
            page.client_storage.set("objectsPage",unique_sweets)
            if len(page.client_storage.get("objectsPage")) % 9 == 0:
                totalPages.value = int(len(page.client_storage.get("objectsPage")) / 9)
            else :
                totalPages.value = int(len(page.client_storage.get("objectsPage")) / 9) + 1
        elif dd.value == "X-MEN comics":
            unique_sweets = []
            [unique_sweets.append(sweet) for sweet in [data for data in requestF for comic in data['comics'] if 'X-MEN' in comic] if sweet not in unique_sweets]
            page.client_storage.set("objectsPage",unique_sweets)
            if len(page.client_storage.get("objectsPage")) % 9 == 0:
                totalPages.value = int(len(page.client_storage.get("objectsPage")) / 9)
            else :
                totalPages.value = int(len(page.client_storage.get("objectsPage")) / 9) + 1

        cards(page.client_storage.get("objectsPage"))

    requestF = PJ.get_data("personajes")()
    page.client_storage.set("objectsPage" ,requestF.copy())
    txt_number =  ft.Text(value="1",text_align="center",width=50)
    totalPages = ft.Text(value=int(len(page.client_storage.get("objectsPage")) / 9),text_align="center",width=50)
    r =  ft.Row(wrap=True, scroll="none", expand=True,)
    
    dd = ft.Dropdown(
        hint_text="Choose your filter",
        text_size= 20,
        alignment=ft.alignment.bottom_center,
        on_change=dropdown_changed,
        options=[
            ft.dropdown.Option("ALL The Characters"),
            ft.dropdown.Option("Characters with comics"),
            ft.dropdown.Option("The *Avengers* comics"),
            ft.dropdown.Option("X-MEN comics"),
        ],
    )

    appbar=ft.AppBar(
            title=ft.Text("Personajes", text_align="center", size=30, color = "#ffb0c9"),
            center_title=True,
            bgcolor=ft.colors.SURFACE_VARIANT,
            actions=[
                ft.Container(
                    content = ft.Row([dd,],alignment = ft.MainAxisAlignment.END,),
                    width = 800,
                    height=300,
                    margin = ft.margin.only(left=0,top=10,right=0,bottom=5),
                    alignment= ft.alignment.bottom_center ,
                ),
            ],
    )

    body = ft.Container(
        ft.Column(
            [
                ft.Container(
                    ft.Stack(
                        #Cuadricula INFO
                        [
                            r
                        ]
                    ),
                    border_radius=8,
                    padding=5,
                    width=800,
                    height=650,
                    alignment= ft.alignment.center,
                ),
                #Fila de flechas pra siguiente pagina
                ft.Row(
                    [
                        ft.IconButton(ft.icons.NAVIGATE_BEFORE_ROUNDED,on_click=before_page),
                        txt_number,
                        ft.IconButton(ft.icons.NAVIGATE_NEXT_ROUNDED,on_click=next_page),
                    ],
                    alignment= ft.MainAxisAlignment.CENTER,
                ),
                ft.Row(
                    [
                        totalPages,
                    ],
                    alignment= ft.MainAxisAlignment.END,
                ),
            ],
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
            alignment= "center",
        ),
        alignment=ft.alignment.center
    )

    cards(page.client_storage.get("objectsPage"))

    return [appbar, body]