import py5



def setup():
    global img
    py5.size(800, 400)
    img = py5.load_image(r"C:\Users\usuario\zambrano-michell-pdi-1c-2026\002 - py5\003 LAB\134157563112116165.jpg")
    img.resize(400, 400)

def draw():
    py5.background(35)

    # Imagen original en la mitad izquierda (sin modificar)
    py5.image(img, 0, 0)

    # Calcular el factor de ajuste según la posición X del mouse
    # remap convierte un valor de un rango a otro
    # Acá: de 0 a 800 píxeles de ancho → de 0 a 2.5 de factor multiplicador
    factor_rojo = py5.remap(py5.mouse_x, 0, py5.width, 0, 2.5)

    # Acceder a la matriz de píxeles del lienzo completo
    img.load_pixels()
    py5.load_pixels()

    for x in range(img.width):
        for y in range(img.height):

            # La imagen es un arreglo lineal. Para acceder al píxel (x, y):
            # índice = x + y * ancho
            indice_img = x + y * img.width
            pixel = img.pixels[indice_img]

            # Separar los canales
            r = py5.red(pixel)
            g = py5.green(pixel)
            b = py5.blue(pixel)

            # Modificar solo el canal rojo según el mouse
            g = g * factor_rojo
            factor_azul = py5.remap(py5.mouse_y, 0, py5.height, 0, 2.5)
            b = b * factor_azul

            # Limitar el valor para que no supere 255
            # Un valor mayor haría que py5 lo interprete incorrectamente
            if r > 255:
                r = 255

            # Calcular el índice del mismo píxel en el lienzo (desplazado 400px a la derecha)
            indice_canvas = (x + 400) + y * py5.width
            py5.pixels[indice_canvas] = py5.color(b, g, r)

    # Aplicar los cambios al lienzo
    py5.update_pixels()

py5.run_sketch()

# Pregutas:
#1. Suprimir el canal rojo por completo: Reemplazá r = r * factor_rojo por r = 0. 
#La imagen de la derecha debería mostrar solo los canales verde y azul. 
#¿Qué pasa con las zonas que eran originalmente rojas?
#Las zonas originalmente rojas ahora tienen tonos verdes o azules, y se ve más oscura la imagen en general.

#2. Intercambiar canales: Cambiá py5.color(r, g, b) por py5.color(b, g, r). 
#Esto intercambia el canal rojo y el azul. Los cielos de color azul deberían volverse rojizos. 
#Pensá qué implica esto: los colores son datos, y cambiar su posición genera una imagen que parece incorrecta pero matemáticamente es válida.
#Al hacer el cambio a bgr, el color cambia totalmente, pero los datos siguen siendo válidos.

#3. Controlar un canal distinto: En lugar de modificar r, aplicá el factor al canal verde (g = g * factor). 
#Considerá también crear un segundo factor que use la posición Y del mouse para controlar el azul.
#Al probar esto de visualizó que dependiendo de cómo se mueva el mouse los colores se mezclan, si es en forma horizontal, la imagen se vuelve roja
#mientras que si se mueve el mouse de forma vertical, la imagen toma un color verde muy brillante.