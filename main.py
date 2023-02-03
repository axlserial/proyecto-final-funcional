from flet import Page,MainAxisAlignment,CrossAxisAlignment,Row,Card,Text,colors,border,border_radius,app,IconButton,Container,Stack,alignment,icons,WEB_BROWSER
import requests as rq


def main(page:  Page):
    page.title = "Flet counter example"
    page.vertical_alignment =  MainAxisAlignment.CENTER
    page.horizontal_alignment =  CrossAxisAlignment.CENTER

    #Funcion que hace la peticion
    def generate_request(url,params):
        response = rq.get(url, params=params)

        if response.status_code == 200:

            return response.json()


    data = generate_request("https://pokeapi.co/api/v2/pokemon/1","")
    txt_number =  Text(value="1",text_align="center",width=50)
    r =  Row(wrap=True, scroll="none", expand=True)
    for i in range(1,16):
        r.controls.append(
            Card(
                content= Container(
                    Text(f"Item {i}"),
                    width=100,
                    height=100,
                    padding=10,
                    alignment= alignment.top_center,
                    bgcolor= colors.RED,
                    border= border.all(1,  colors.RED_400),
                    border_radius= border_radius.all(5),
                ),
                width=200,
                height=200,
            )
        )
    
    #Funcion de control de paginas
    def next_page(e):
        r.controls.clear()
        if int(txt_number.value) <= 2:
            txt_number.value = int(txt_number.value) +1
            for i in range(1+((int(txt_number.value)-1)*15),(int(txt_number.value)*15)+1):
                r.controls.append(
                    Card(
                        content= Container(
                            Text(f"Item {i}"),
                            width=100,
                            height=100,
                            padding=10,
                            alignment= alignment.top_center,
                            bgcolor= colors.RED,
                            border= border.all(1,  colors.RED_400),
                            border_radius= border_radius.all(5),
                        ),
                        width=200,
                        height=200,
                    )
                )
            page.update()
        else:
            txt_number.value = 1
            for i in range(1,16):
                r.controls.append(
                    Card(
                        content= Container(
                            Text(f"Item {i}"),
                            width=100,
                            height=100,
                            padding=10,
                            alignment= alignment.top_center,
                            bgcolor= colors.RED,
                            border= border.all(1,  colors.RED_400),
                            border_radius= border_radius.all(5),
                        ),
                        width=200,
                        height=200,
                    )
                )
            page.update()

    def before_page(e):
        r.controls.clear()
        if int(txt_number.value) == 1:
            txt_number.value = 3
            for i in range(1+((int(txt_number.value)-1)*15),(int(txt_number.value)*15)+1):
                r.controls.append(
                    Card(
                        content= Container(
                            Text(f"Item {i}"),
                            width=100,
                            height=100,
                            padding=10,
                            alignment= alignment.top_center,
                            bgcolor= colors.RED,
                            border= border.all(1,  colors.RED_400),
                            border_radius= border_radius.all(5),
                        ),
                        width=200,
                        height=200,
                    )
                )
            page.update()
        
        else:
            txt_number.value = int(txt_number.value) - 1
            for i in range(1+((int(txt_number.value)*15)-15),(int(txt_number.value)*15)+1):
                r.controls.append(
                    Card(
                        content= Container(
                            Text(f"Item {i}"),
                            width=100,
                            height=100,
                            padding=10,
                            alignment= alignment.top_center,
                            bgcolor= colors.RED,
                            border= border.all(1,  colors.RED_400),
                            border_radius= border_radius.all(5),
                        ),
                        width=200,
                        height=200,
                    )
                )
            page.update()


    
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
            width=1000,
            height=840,
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



app(target=main, view=WEB_BROWSER)