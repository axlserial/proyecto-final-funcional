from flet import Page,MainAxisAlignment,CrossAxisAlignment,Row,Card,Text,colors,border,border_radius,app,IconButton,Container,Stack,alignment,icons,WEB_BROWSER,Column,ListTile,Image,ImageFit,TextAlign
import requests as rq
import services.personajes as PJ

def main(page:  Page):

    page.title = "Flet counter example"
    page.vertical_alignment =  MainAxisAlignment.CENTER
    page.horizontal_alignment =  CrossAxisAlignment.CENTER

    requestF = PJ.get_data("personajes")()
    print(len(requestF))
    #Funcion de control de paginas
    def next_page(e):
        r.controls.clear()
        if int(txt_number.value) <= 6:
            txt_number.value = int(txt_number.value) +1
            cards()
        else:
            txt_number.value = 1
            cards()

    def before_page(e):
        r.controls.clear()
        if int(txt_number.value) == 1:
            txt_number.value = 7
            cards()
        
        else:
            txt_number.value = int(txt_number.value) - 1
            cards()

    def cards():
        for i in range((int(txt_number.value)*10)-9,(int(txt_number.value)*10)):
            r.controls.append(
                Card(
                    Container(
                        Column(
                            [
                                Text(requestF[i-1]["nombre"], text_align = "center" , selectable=False),
                                Image(
                                    src=requestF[i-1]['imagen'],
                                    width=100,
                                    height=100,
                                ),
                                Text(requestF[i-1]["id"],selectable=False,text_align = "center"), 
                                Text(requestF[i-1]["descripcion"],selectable=False,text_align = "center"),
                            ],
                            alignment=MainAxisAlignment.CENTER,
                            horizontal_alignment = CrossAxisAlignment.CENTER,
                        ),
                        bgcolor= colors.RED,
                        border= border.all(1,  colors.RED_400),
                        border_radius= border_radius.all(5),
                        alignment = alignment.center,
                    ),
                    
                    width=200,
                    height=200,
                )
            )

        page.update()


    txt_number =  Text(value="1",text_align="center",width=50)
    r =  Row(wrap=True, scroll="none", expand=True)
    cards()


    
    page.add(
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
            height=900,
            bgcolor= colors.WHITE,
            alignment= alignment.top_center,
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
    )



app(target=main)