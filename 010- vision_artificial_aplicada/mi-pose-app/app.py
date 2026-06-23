#app desplegada en hugging face https://huggingface.co/spaces/michellzambrano/detector-pose-tp
# app.py — Detector de Pose con MediaPipe
# Estructura: 3 capas (Data Layer / Business Logic / Presentation Layer)

import mediapipe as mp
import gradio as gr
import numpy as np


# ─────────────────────────────────────────────────────────────────────────
# CAPA 1 — DATA LAYER
# El modelo se carga una sola vez cuando arranca la aplicación.
# Si lo cargáramos dentro de la función, cada request esperaría la carga.
# ─────────────────────────────────────────────────────────────────────────

modulo_pose    = mp.solutions.pose
modulo_dibujo  = mp.solutions.drawing_utils
estilos_dibujo = mp.solutions.drawing_styles

# TODO: completá los parámetros con los valores que encontraron en la exploración
detector_pose = modulo_pose.Pose(
    static_image_mode=True,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

# ─────────────────────────────────────────────────────────────────────────
# CAPA 2 — BUSINESS LOGIC
# Toda la lógica de procesamiento vive acá, desacoplada de la interfaz.
# Si mañana cambian la UI de Gradio a otra tecnología, esta función no cambia.
# ─────────────────────────────────────────────────────────────────────────

def detectar_pose(imagen_entrada):

    resultado = detector_pose.process(imagen_entrada)

    imagen_anotada = imagen_entrada.copy()

    if resultado.pose_landmarks is None:
        mensaje = "No se detectó ninguna figura humana en la imagen."
        return imagen_anotada, mensaje

    modulo_dibujo.draw_landmarks(
        image=imagen_anotada,
        landmark_list=resultado.pose_landmarks,
        connections=modulo_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=estilos_dibujo.get_default_pose_landmarks_style()
    )

    lista_landmarks = resultado.pose_landmarks.landmark

    punto_hombro_derecho = lista_landmarks[12]
    punto_hombro_izquierdo = lista_landmarks[11]
    punto_cadera_derecha = lista_landmarks[24]

    punto_rodilla_derecha = lista_landmarks[26]
    punto_rodilla_izquierda = lista_landmarks[25]

    distancia_hombros = abs(
        punto_hombro_derecho.x -
        punto_hombro_izquierdo.x
    )

    distancia_hombros_redondeada = round(
        distancia_hombros, 3
    )

    distancia_torso = abs(
        punto_hombro_derecho.y -
        punto_cadera_derecha.y
    )

    distancia_torso = round(distancia_torso, 3)

    linea_hombros = (
        f"Distancia entre hombros: "
        f"{distancia_hombros_redondeada}"
    )

    linea_visibilidad = (
        f"Visibilidad hombro derecho: "
        f"{round(punto_hombro_derecho.visibility, 2)}"
    )

    linea_cadera = (
        f"Cadera derecha y="
        f"{round(punto_cadera_derecha.y, 3)}"
    )

    linea_torso = (
        f"Distancia hombro-cadera: "
        f"{distancia_torso}"
    )

    linea_rodilla = (
        f"Visibilidad rodilla derecha: "
        f"{round(punto_rodilla_derecha.visibility, 2)}"
    )

    texto_info = (
        linea_hombros + "\n" +
        linea_visibilidad + "\n" +
        linea_cadera + "\n" +
        linea_torso + "\n" +
        linea_rodilla
    )

    return imagen_anotada, texto_info


# ─────────────────────────────────────────────────────────────────────────
# CAPA 3 — PRESENTATION LAYER
# La interfaz declara cómo se ve la app, sin lógica de negocio adentro.
# ─────────────────────────────────────────────────────────────────────────

with gr.Blocks(title="Detector de Pose") as aplicacion:

    gr.Markdown("## Detector de Pose corporal — MediaPipe")
    gr.Markdown(
        "Subí una imagen de una persona y el modelo va a detectar "
        "los 33 puntos clave del esqueleto corporal."
    )

    with gr.Row():
        # TODO: definí los componentes de entrada
        # Pista: gr.Image con type="numpy" y un label descriptivo
        entrada_imagen = gr.Image(
            type="numpy",
            label="Fotografía"
   )

    with gr.Row():
        # TODO: definí los dos componentes de salida
        # Pista: imagen anotada + cuadro de texto con métricas
        salida_imagen = gr.Image(
            label="Pose detectada"
        )
        salida_texto = gr.Textbox(
            label="Información de puntos clave"
        )

    boton_analizar = gr.Button("Analizar pose", variant="primary")

    boton_analizar.click(
        fn=detectar_pose,
        inputs=entrada_imagen,
        outputs=[salida_imagen, salida_texto]
    )


if __name__ == "__main__":
    aplicacion.launch(server_name="0.0.0.0", server_port=7860)