# Proyecto: API de Predicción de Importaciones

Este proyecto contiene la extracción del modelo de regresión lineal entrenado desde el notebook, su empaquetado en un paquete instalable (.whl), y una API FastAPI lista para usar.

## Estructura del Proyecto

```text
.
├── train_model.py                    # Script para entrenar y guardar el modelo
├── modelo_paquete/                   # Paquete Python instalable
│   ├── setup.py                      # Configuración del paquete
│   ├── README.md                     # Documentación del paquete
│   └── modelo_importaciones/         # Módulo del paquete
│       ├── __init__.py
│       ├── modelo.py                 # Clase para usar el modelo
│       └── model/                    # Directorio con el modelo entrenado
│           ├── modelo_regresion_lineal.pkl
│           └── modelo_info.pkl
├── api/                              # API FastAPI (desarrollo local)
│   ├── main.py                       # Aplicación FastAPI principal
│   ├── requirements.txt              # Dependencias de la API
│   ├── ejemplo_uso.py                # Ejemplos de uso
│   ├── README.md                     # Documentación de la API
│   └── deploy_api/                   # Carpeta para despliegue en EC2 Ubuntu
│       ├── main.py                   # Aplicación FastAPI
│       ├── requirements.txt          # Dependencias
│       ├── modelo_importaciones-1.0.0-py3-none-any.whl  # Modelo entrenado
│       ├── setup-ubuntu.sh           # Script de instalación automática
│       └── README.md                 # Guía de despliegue
└── notebooks/                        # Notebooks originales
    └── Importaciones2024.csv         # Datos de entrenamiento
```

## Pasos para Usar el Proyecto

### Paso 1: Entrenar y Guardar el Modelo

Primero, necesitas entrenar el modelo y guardarlo en el directorio del paquete:

```bash
python train_model.py
```

Este script:

- Carga y preprocesa los datos desde `notebooks/Importaciones2024.csv`
- Entrena el modelo de regresión lineal con las 4 variables principales
- Guarda el modelo en `modelo_paquete/modelo_importaciones/model/`

### Paso 2: Construir el Paquete Instalable (.whl)

Una vez que el modelo esté guardado, construye el paquete:

```bash
cd modelo_paquete
python setup.py bdist_wheel
```

Esto creará el archivo `.whl` en `modelo_paquete/dist/modelo_importaciones-1.0.0-py3-none-any.whl`

### Paso 3: Instalar el Paquete

Instala el paquete en tu entorno:

```bash
pip install modelo_paquete/dist/modelo_importaciones-1.0.0-py3-none-any.whl
```

O desde el directorio `modelo_paquete`:

```bash
pip install dist/modelo_importaciones-1.0.0-py3-none-any.whl
```

### Paso 4: Instalar Dependencias de la API

```bash
cd api
pip install -r requirements.txt
```

### Paso 5: Ejecutar la API

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

## Uso de la API

### Endpoint Principal: /predict

El endpoint `/predict` acepta 4 parámetros:

1. **mes** (int): Mes del año (1-12)
2. **pais_pro** (str): País de origen (ej: "América", "Asia", "Europa", "África", "Oceanía")
3. **aduana** (str): Tipo de aduana ("Maritima y Fluvial" o "Aereas y Terrestres")
4. **tipo_importacion** (str): Tipo de importación (ej: "Importación ordinaria", "Importación con franquicia", etc.)

**Ejemplo de solicitud:**

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

### Otros Endpoints

- **GET /** - Información de la API
- **GET /health** - Estado de la API
- **GET /info** - Información del modelo y categorías disponibles
- **GET /docs** - Documentación interactiva (Swagger UI)
- **GET /redoc** - Documentación alternativa (ReDoc)

## Ejemplo de Uso con Python

Puedes usar el script de ejemplo incluido:

```bash
cd api
python ejemplo_uso.py
```

O usar directamente el paquete:

```python
from modelo_importaciones import ModeloImportaciones

# Cargar el modelo
modelo = ModeloImportaciones()

# Realizar una predicción
prediccion = modelo.predecir(
    mes=5,
    pais_pro="América",
    aduana="Maritima y Fluvial",
    tipo_importacion="Importación ordinaria"
)

print(f"Valor CIF predicho: {prediccion:.2f} USD/kg")
```

## Despliegue en EC2 Ubuntu

Para desplegar la API en una instancia EC2 con Ubuntu, usa la carpeta `api/deploy_api/`:

1. Transfiere la carpeta `api/deploy_api/` a tu EC2
2. Ejecuta el script de instalación: `./setup-ubuntu.sh`
3. La API se ejecutará en el puerto 8001

Ver `api/deploy_api/README.md` para instrucciones detalladas.

## Características Importantes

- **El modelo NO se reentrena** - Solo se carga desde el paquete instalado
- **Listo para producción** - Estructura completa con FastAPI y uvicorn
- **Validación de entrada** - Usa Pydantic para validar los parámetros
- **Documentación automática** - Swagger UI y ReDoc incluidos
- **Manejo de errores** - Respuestas HTTP apropiadas para errores
- **Despliegue en EC2** - Carpeta `api/deploy_api/` lista para producción  

## Notas

- Asegúrate de ejecutar `train_model.py` antes de construir el paquete
- El modelo debe estar en `modelo_paquete/modelo_importaciones/model/` antes de construir el .whl
- El paquete .whl puede ser instalado en cualquier entorno Python compatible
- La API local (`api/`) usa el puerto 8000
- La API de despliegue (`api/deploy_api/`) usa el puerto 8001 y está optimizada para EC2 Ubuntu
- La carpeta `api/deploy_api/` contiene todo lo necesario para desplegar sin reentrenar el modelo

## Solución de Problemas

### Error: "No se encontró el modelo"

Asegúrate de haber ejecutado `train_model.py` primero y que el modelo esté en la ubicación correcta.

### Error: "ModuleNotFoundError: modelo_importaciones"

Asegúrate de haber instalado el paquete .whl con `pip install`.

### Error al ejecutar la API

Verifica que todas las dependencias estén instaladas:

```bash
pip install -r api/requirements.txt
```
