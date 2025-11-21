# API de Predicción de Importaciones

API FastAPI para predecir el valor CIF de importaciones usando el modelo de regresión lineal empaquetado.

## Instalación

1. Asegúrate de tener instalado el paquete del modelo:

```bash
# Desde el directorio raíz del proyecto
cd modelo_paquete
python setup.py bdist_wheel
pip install dist/modelo_importaciones-1.0.0-py3-none-any.whl
```

2. Instala las dependencias de la API:

```bash
cd api
pip install -r requirements.txt
```

## Ejecución

Para ejecutar la API con uvicorn:

```bash
cd api
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

O simplemente:

```bash
cd api
python main.py
```

La API estará disponible en: `http://localhost:8000`

## Documentación Interactiva

Una vez que la API esté corriendo, puedes acceder a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Endpoints

### GET /

Endpoint raíz con información de la API.

### GET /health

Verifica el estado de la API y si el modelo está cargado.

**Ejemplo de respuesta:**
```json
{
  "status": "healthy",
  "modelo_cargado": true
}
```

### GET /info

Obtiene información sobre el modelo y las categorías disponibles.

**Ejemplo de respuesta:**
```json
{
  "paises_disponibles": ["América", "Asia", "Europa", ...],
  "aduanas_disponibles": ["Maritima y Fluvial", "Aereas y Terrestres"],
  "tipos_disponibles": ["Importación ordinaria", ...],
  "metricas": {
    "MAE": 3108.22,
    "RMSE": 27225.45,
    "R2": 0.9591
  }
}
```

### POST /predict

Realiza una predicción del valor CIF usando el modelo entrenado.

**Parámetros de entrada:**
- `mes` (int): Mes del año (1-12)
- `pais_pro` (str): País de origen (ej: "América", "Asia", "Europa")
- `aduana` (str): Tipo de aduana ("Maritima y Fluvial" o "Aereas y Terrestres")
- `tipo_importacion` (str): Tipo de importación (ej: "Importación ordinaria")

**Ejemplo de solicitud:**
```json
{
  "mes": 5,
  "pais_pro": "América",
  "aduana": "Maritima y Fluvial",
  "tipo_importacion": "Importación ordinaria"
}
```

**Ejemplo de respuesta:**
```json
{
  "prediccion": 12345.67,
  "mes": 5,
  "pais_pro": "América",
  "aduana": "Maritima y Fluvial",
  "tipo_importacion": "Importación ordinaria"
}
```

## Ejemplo de Uso

Puedes usar el script `ejemplo_uso.py` para probar la API:

```bash
# Asegúrate de que la API esté corriendo en otra terminal
python ejemplo_uso.py
```

O usar curl:

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "mes": 5,
    "pais_pro": "América",
    "aduana": "Maritima y Fluvial",
    "tipo_importacion": "Importación ordinaria"
  }'
```

## Notas

- El modelo NO se reentrena al usar la API, solo se carga desde el paquete instalado.
- Asegúrate de haber ejecutado `train_model.py` antes de construir el paquete.
- El modelo debe estar en `modelo_paquete/modelo_importaciones/model/` antes de construir el .whl.

