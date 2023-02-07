from flet import Page,MainAxisAlignment,CrossAxisAlignment,Row,Card,Text,AppBar,border,border_radius,IconButton,Container,Stack,alignment,icons,Column,Image,Dropdown,dropdown,margin,theme,colors
import services.personajes as PJ
from typing import Callable

def characters_view(update_func: Callable, page : Page):
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
                for i in range(((-9)+(int(txt_number.value)*9))+1, (len(cardsPage))+1):
                    r.controls.append(
                        Card(
                            Container(
                                Column(
                                    [
                                        Text(cardsPage[i-1]["nombre"],color = "#381e72", text_align = "center" , selectable=False , ),
                                        Image(
                                            src=cardsPage[i-1]['imagen'],
                                            width=100,
                                            height=100,
                                        ),
                                        Text(cardsPage[i-1]["id"],color = "#381e72",selectable=False,text_align = "center", ), 
                                        Text(cardsPage[i-1]["descripcion"][:23]+"...",color = "#381e72",selectable=False,text_align = "center",),
                                    ],
                                    alignment=MainAxisAlignment.CENTER,
                                    horizontal_alignment = CrossAxisAlignment.CENTER,
                                ),
                                bgcolor= "#cfbcff",
                                border= border.all(1,  "#C4ACFF"),
                                border_radius= border_radius.all(5),
                                alignment = alignment.center,
                            ),
                            width=200,
                            height=200,
                        )
                    )
            else:
                for i in range(((-9)+(int(txt_number.value)*9))+1 ,(int(txt_number.value)*9)+1):
                    r.controls.append(
                        Card(
                            Container(
                                Column(
                                    [
                                        Text(cardsPage[i-1]["nombre"],color = "#381e72", text_align = "center" , selectable=False , ),
                                        Image(
                                            src=cardsPage[i-1]['imagen'],
                                            width=100,
                                            height=100,
                                        ),
                                        Text(cardsPage[i-1]["id"],color = "#381e72",selectable=False,text_align = "center" , ), 
                                        Text(cardsPage[i-1]["descripcion"][:23]+"...",color = "#381e72",selectable=False,text_align = "center", ),
                                    ],
                                    alignment=MainAxisAlignment.CENTER,
                                    horizontal_alignment = CrossAxisAlignment.CENTER,
                                ),
                                bgcolor= "#cfbcff",
                                border= border.all(1, "#C4ACFF"),
                                border_radius= border_radius.all(5),
                                alignment = alignment.center,
                            ),
                            width=200,
                            height=200,
                        )
                    )
        else:
            r.controls.append(
                Card(
                    Container(
                        Column(
                            [
                                Text("No hay personajes", text_align = "center" ,color = "#381e72", selectable=False ),
                            ],
                            alignment=MainAxisAlignment.CENTER,
                            horizontal_alignment = CrossAxisAlignment.CENTER,
                        ),
                        bgcolor= "#ffb4ab",
                        border= border.all(1,"#FCA196"),
                        border_radius= border_radius.all(5),
                        alignment = alignment.center,
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
    dd = Dropdown(
        hint_text="Choose your filter",
        alignment=alignment.bottom_center,
        on_change=dropdown_changed,
        options=[
            dropdown.Option("ALL The Characters"),
            dropdown.Option("Characters with comics"),
            dropdown.Option("The *Avengers* comics"),
            dropdown.Option("X-MEN comics"),
        ],
    )
    page.client_storage.set("objectsPage" ,requestF.copy())
    txt_number =  Text(value="1",text_align="center",width=50)
    totalPages = Text(value=int(len(page.client_storage.get("objectsPage")) / 9),text_align="center",width=50)
    r =  Row(wrap=True, scroll="none", expand=True,)

    appbar=AppBar(
            title=Text("Personajes", text_align="center", size=30, color = "#ffb0c9"),
            center_title=True,
            bgcolor=colors.SURFACE_VARIANT,
            actions=[
                Container(
                    content = Row([dd,],alignment = MainAxisAlignment.END,),
                    width = 800,
                    height=300,
                    margin = margin.only(left=0,top=10,right=0,bottom=5),
                    alignment= alignment.bottom_center ,
                ),
            ],
    ),
    body = Column(horizontal_alignment = CrossAxisAlignment.CENTER,alignment= "center",)
    body.controls = [
        Container(
            Stack(
                #Cuadricula INFO
                [
                    r
                ]
            ),
            border_radius=8,
            padding=5,
            width=800,
            height=650,
            alignment= alignment.center,
        ),
        #Fila de flechas pra siguiente pagina
        Row(
            [
                IconButton(icons.NAVIGATE_BEFORE_ROUNDED,on_click=before_page),
                txt_number,
                IconButton(icons.NAVIGATE_NEXT_ROUNDED,on_click=next_page),
            ],
            alignment= MainAxisAlignment.CENTER,
        ),
        Row(
            [
                totalPages,
            ],
            alignment= MainAxisAlignment.END,
        ),
    ]

    cards(page.client_storage.get("objectsPage"))

    return [appbar, body]