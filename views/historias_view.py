import flet as ft
from typing import Callable
import services.historias_service as PJ
from utils import COLOR_PALETTE

def stories_view(update_func: Callable, page : ft.Page):
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
                                        ft.Text(cardsPage[i-1]["id"],color = "#381e72",selectable=False,text_align = "center" ,size=12 , ),
                                        ft.Text(cardsPage[i-1]["comics"][0],color = "#381e72", text_align = "justify" , selectable=False , ),
                                    ],
                                    alignment=ft.MainAxisAlignment.START,
                                    horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                                ),
                                bgcolor= "#cfbcff",
                                border= ft.border.all(1,  "#C4ACFF"),
                                padding= ft.padding.only(left=10,top = 10 , right= 10, bottom= 0),
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
                                        ft.Text(cardsPage[i-1]["id"],color = "#381e72",selectable=False,text_align = "center" , size=12 ,),
                                        ft.Text(cardsPage[i-1]["comics"][0],color = "#381e72", text_align = "justify" , selectable=False , ),
                                    ],
                                    alignment=ft.MainAxisAlignment.START,
                                    horizontal_alignment = ft.CrossAxisAlignment.CENTER,
                                ),
                                bgcolor= "#cfbcff",
                                border= ft.border.all(1, "#C4ACFF"),
                                padding= ft.padding.only(left=10,top = 10 , right= 10, bottom= 0),
                                border_radius= ft.border_radius.all(5),
                                alignment = ft.alignment.center,
                            ),
                            width=200,
                            height=200,
                        ),
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
                        bgcolor= "#ffb4ab",
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
        page.update()

        if dd.value == "ALL The Stories":
            page.client_storage.set("objectsPage", requestF.copy())
            totalPages.value = int(len(page.client_storage.get("objectsPage")) / 9)
        elif dd.value == "Written by Larry Hama":
            unique_sweets = []
            [unique_sweets.append(sweet) for sweet in [data for data in requestF for comic in data['Creadores'] if 'Larry Hama' in comic] if sweet not in unique_sweets]
            page.client_storage.set("objectsPage",unique_sweets)
            if len(page.client_storage.get("objectsPage")) % 9 == 0:
                totalPages.value = int(len(page.client_storage.get("objectsPage")) / 9)
            else :
                totalPages.value = int(len(page.client_storage.get("objectsPage")) / 9) + 1
        elif dd.value == "The *Avengers* stories":
            unique_sweets = []
            [unique_sweets.append(sweet) for sweet in [data for data in requestF for comic in data['Series'] if 'Avengers' in comic] if sweet not in unique_sweets]
            page.client_storage.set("objectsPage",unique_sweets)
            if len(page.client_storage.get("objectsPage")) % 9 == 0:
                totalPages.value = int(len(page.client_storage.get("objectsPage")) / 9)
            else :
                totalPages.value = int(len(page.client_storage.get("objectsPage")) / 9) + 1
        elif dd.value == "X-MEN stories":
            unique_sweets = []
            [unique_sweets.append(sweet) for sweet in [data for data in requestF for comic in data['comics'] if 'X-MEN' in comic] if sweet not in unique_sweets]
            page.client_storage.set("objectsPage",unique_sweets)
            if len(page.client_storage.get("objectsPage")) % 9 == 0:
                totalPages.value = int(len(page.client_storage.get("objectsPage")) / 9)
            else :
                totalPages.value = int(len(page.client_storage.get("objectsPage")) / 9) + 1

        cards(page.client_storage.get("objectsPage"))


    requestF = PJ.get_data("stories")()
    page.client_storage.set("objectsPage" ,requestF.copy())
    txt_number =  ft.Text(value="1",text_align="center",width=50)
    totalPages = ft.Text(value=int(len(page.client_storage.get("objectsPage")) / 9),text_align="center",width=50)
    r =  ft.Row(wrap=True, scroll="none", expand=True,)
    dd = ft.Dropdown(
        width=250,
        alignment=ft.alignment.top_right,
        hint_text="Choose your filter",
        text_size= 20,
        on_change=dropdown_changed,
        options=[
            ft.dropdown.Option("ALL The Stories"),
            ft.dropdown.Option("Written by Larry Hama"),
            ft.dropdown.Option("The *Avengers* stories"),
            ft.dropdown.Option("X-MEN stories"),
        ],
    )

    
    appbar=ft.AppBar(
            title=ft.Text("Historias", text_align="center", size=30, color = "#ffb0c9"),
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

    body =  ft.Container(
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
            alignment = 'center',
        ),
    )

    cards(page.client_storage.get("objectsPage"))

    return [appbar, body]


