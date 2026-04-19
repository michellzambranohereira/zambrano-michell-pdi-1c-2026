import py5

img = None

def setup():
    global img
    py5.size(800, 400)
    img = py5.load_image(r"C:\Users\usuario\zambrano-michell-pdi-1c-2026\002 - py5\003 LAB\134160935775034328.jpg")  # Usá una imagen disponible en tu carpeta img/
    img.resize(400, 400)

def draw():
    py5.background(255)

    # Mostrar la imagen en la mitad izquierda
    py5.image(img, 0, 0)

    # Limitar las coordenadas del mouse al área de la imagen
    # Esto evita errores si el cursor sale de la imagen
    mx = py5.constrain(py5.mouse_x, 0, 399)
    my = py5.constrain(py5.mouse_y, 0, 399)

    # Obtener el color del píxel en esa posición
    color_pixel = py5.get_pixels(int(mx), int(my))

    # Separar el color en sus tres canales
    r = py5.red(color_pixel)
    g = py5.green(color_pixel)
    b = py5.blue(color_pixel)

    # Mostrar el color como un cuadrado en la mitad derecha (la "lupa")
    py5.fill(255 - r, 255 - g, 255 - b)
    py5.stroke(0)
    py5.rect(450, 50, 300, 300)

    # Mostrar los valores numéricos
    py5.fill(0)
    py5.text_size(18)
    py5.text(f"Posición: ({mx}, {my})", 450, 30)
    py5.text(f"R: {r:.0f}   G: {g:.0f}   B: {b:.0f}", 450, 380)

py5.run_sketch()

# Pregutas:
#1. Color negativo: Reemplazá py5.fill(color_pixel) por py5.fill(255 - r, 255 - g, 255 - b). El color del cuadrado debería ser el complementario del píxel original. 
#¿Qué color aparece sobre un rojo puro? ¿Y sobre el blanco?
#En el rojo puro aparecen colores azules, unos más claros y otros más oscuros dependiendo de donde se posicione el mouse.
#En el blanco el color que da el recuadro es negro.

#2. Aislamiento de canal: Ahora usá py5.fill(r, 0, 0). Esto elimina verde y azul y muestra solo la contribución del canal rojo. 
#Pasá el cursor por zonas azules o verdes de la imagen y observá cuánto rojo tienen en realidad.
#Se puede observar que a medida que se mueve el mouse, cada pixel de la imagen muestra que incluso teniendo un color predominate, pueden igual contener cierta cantidad de color rojo.

#3. Sin protección: Comentá la línea con py5.constrain() reemplazándola por mx = py5.mouse_x y my = py5.mouse_y. Mové el mouse fuera de la imagen rápidamente. 
#¿Qué mensaje de error aparece en la terminal? ¿Qué tipo de error es?
#Dependiento de cómo se reemplaza la línea de código pueden surgir dos errores:
#Si se deja mx = py5.constrain y se reemplaza solo lo que está dentro del paréntesis por mx = py5.mouse_x y my = py5.mouse_y
#da el error TypeError: constrain() got an unexpected keyword argument 'mx' es decir mx no existe como parámetro
#En cambio si se reemplaza toda la línea y se deja solo mx = py5.mouse_x y my = py5.mouse_y, podemos ver que ahora el mouse se sale de la imágen y empieza a tomar colores fuera del área que estaba delimitada.
