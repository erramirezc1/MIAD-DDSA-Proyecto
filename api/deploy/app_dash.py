import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# 3) App con Dash
app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "Análisis predictivo de importaciones 2024"
server = app.server
app.config.suppress_callback_exceptions = True

# URL base de la API de predicción
API_URL = os.getenv("API_URL", "http://localhost:8001")

# Definicion de UI
PRIMARY = "#0D4C5E"
LIGHT = "#F5F7F9"
BOX_WIDTH = 420

HEADER = html.Div(
    style={
        "background": PRIMARY,
        "color": "#fff",
        "padding": "14px 20px",
        "borderRadius": "8px",
        "marginBottom": "16px",
    },
    children=[
        html.H3(
            "Análisis predictivo de importaciones colombianas en 2024",
            style={"margin": "0"},
        )
    ],
)

INTRO = html.Div(
    "Ingrese las variables relacionadas a la importación y obtenga una estimación del valor CIF en USD/kg.",
    style={
        "maxWidth": "900px",
        "margin": "8px auto 22px",
        "textAlign": "center",
        "color": "#10151a",
    },
)

BTN_STYLE = {
    "background": PRIMARY,
    "color": "#fff",
    "fontWeight": "700",
    "padding": "10px 18px",
    "border": "none",
    "borderRadius": "8px",
    "width": f"{BOX_WIDTH}px",
    "cursor": "pointer",
}

RESULT_STYLE = {
    "border": "2px solid #05704B",
    "background": LIGHT,
    "padding": "14px 18px",
    "borderRadius": "8px",
    "textAlign": "center",
    "fontWeight": "700",
    "fontSize": "22px",
    "width": f"{BOX_WIDTH}px",
    "margin": "0 auto",
}

# Opciones para controles UI
Paises_UI = [
    "China",
    "Estados Unidos",
    "México",
    "Brasil",
    "Alemania",
    "India",
    "Corea del Sur",
]

# Mapeo de país mostrado en UI a continente que espera la API
PAIS_TO_CONTINENTE = {
    "China": "Asia",
    "India": "Asia",
    "Corea del Sur": "Asia",
    "Alemania": "Europa",
    "Estados Unidos": "America",
    "México": "America",
    "Brasil": "America",
}

# Lista de aduanas agrupadas para UI
ADUANAS_UI = ["Maritima y Fluvial", "Aereas y Terrestres"]

# Lista de tipos de importación para UI
Tipos_UI = ["Ordinaria", "Franquicia", "Temporal", "Reimportación"]
MAP_TIPO = {
    "Ordinaria": "Importación ordinaria",
    "Franquicia": "Importación con franquicia",
    "Temporal": "Importación temporal",
    "Reimportación": "Reimportación",
}

# Layout de la app
app.layout = html.Div(
    style={"padding": "16px"},
    children=[
        HEADER,
        INTRO,
        html.Div(
            style={
                "display": "flex",
                "gap": "28px",
                "alignItems": "flex-start",
                "justifyContent": "space-between",
                "flexWrap": "wrap",
            },
            children=[
                html.Div(
                    [
                        html.H4("Mes"),
                        dcc.Dropdown(
                            id="ddl-mes",
                            options=[{"label": m, "value": m} for m in range(1, 13)],
                            value=5,
                            clearable=False,
                            style={"minWidth": "140px"},
                        ),
                    ]
                ),
                html.Div(
                    [
                        html.H4("País de origen"),
                        dcc.Dropdown(
                            id="ddl-pais",
                            options=[{"label": p, "value": p} for p in Paises_UI],
                            value="China",
                            clearable=False,
                            style={"minWidth": "220px"},
                        ),
                    ]
                ),
                html.Div(
                    [
                        html.H4("Aduana"),
                        dcc.Dropdown(
                            id="ddl-aduana",
                            options=[{"label": a, "value": a} for a in ADUANAS_UI],
                            value="Maritima y Fluvial",
                            clearable=False,
                            style={"minWidth": "220px"},
                        ),
                    ]
                ),
                html.Div(
                    [
                        html.H4("Tipo importación"),
                        dcc.Dropdown(
                            id="ddl-tipo",
                            options=[{"label": t, "value": t} for t in Tipos_UI],
                            value="Ordinaria",
                            clearable=False,
                            style={"minWidth": "220px"},
                        ),
                    ]
                ),
            ],
        ),
        html.Br(),
        html.Div(
            style={"textAlign": "center"},
            children=[
                html.Button(
                    "Predecir valor CIF",
                    id="btn-predict",
                    n_clicks=0,
                    style=BTN_STYLE,
                )
            ],
        ),
        html.Br(),
        html.Div(id="pred-output", style=RESULT_STYLE),
    ],
)

# Callback para realizar la predicción al hacer clic en el botón
@app.callback(
    Output("pred-output", "children"),
    Input("btn-predict", "n_clicks"),
    State("ddl-mes", "value"),
    State("ddl-pais", "value"),
    State("ddl-aduana", "value"),
    State("ddl-tipo", "value"),
    prevent_initial_call=True,
)
def predict_value(n_clicks, mes, pais_ui, aduana, tipo_ui):
    if n_clicks is None:
        return dash.no_update

    tipo_model = MAP_TIPO.get(tipo_ui, tipo_ui)
    # Convertir país de UI a continente que espera la API
    pais_pro = PAIS_TO_CONTINENTE.get(pais_ui, pais_ui)

    payload = {
        "mes": mes,
        "pais_pro": pais_pro,        
        "aduana": aduana,      
        "tipo_importacion": tipo_model
    }

    try:
        resp = requests.post(f"{API_URL}/predict", json=payload, timeout=5)
    except requests.RequestException as e:
        print("Error de conexión con la API:", e)
        return "No fue posible comunicarse con la API. Revise la URL y que el servicio esté activo."

    if resp.status_code != 200:
        print("Error de la API, status:", resp.status_code, "cuerpo:", resp.text)
        return f"Error de la API. Código {resp.status_code}."

    try:
        data = resp.json()
    except ValueError:
        return "La API respondió en un formato que no es JSON válido."

    pred = data.get("prediccion")
    if pred is None:
        return "La API no devolvió el campo 'prediccion'."

    try:
        pred_float = float(pred)
    except (TypeError, ValueError):
        return "La API devolvió una predicción que no es numérica."

    return f"{pred_float:,.0f} USD/kg"

# Ejecutar la app
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)

