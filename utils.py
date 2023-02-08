from oslash import do, read_file, let, List


def to_List():
    def _to_List(*x):
        return List.from_iterable(x)
    return _to_List



# Leemos el contenido del archivo
lectura = do(
    let(file = read_file("assets/files/color_palette.txt"))
)

# l = lambda *items: List.from_iterable(items)

l = to_List()

# la variable archivo de tipo <class 'oslash.list.Cons'> tiene el contenido del archivo el cual es un string
archivo = do( let(name = l(lectura())))


# Separamos el 'string' por saltos de línea para que obtengamos cada linea del archivo
# como elementos de una lista con ayuda del metodo map() de la clase List
archivo_elementos = archivo.map(lambda x: x.split('\n'))

# En archivo_elementos tenemos una lista de listas con un solo elemento → [['','','',...]]
# para obtener la lista de elementos usamos el metodo head de la clase List → ['','','',...]
# y la retornamos


lista_archivo = archivo_elementos.head()

# De la lista obtenida, debemos separar cada elemento en 2 partes → ['nombre_color:valor_hexadecimal',...]
# creamos un generador para obtener una lista de tuplas
# donde cada tupla tendra com elementos el nombre del color y su valor en hexadecimal
colores_gen = (tuple(color.split(":")) for color in lista_archivo if color != "")

# Creamos un diccionario que tendra como clave el nombre del color y como valor su valor en hexadecimal

COLOR_PALETTE = dict(colores_gen)