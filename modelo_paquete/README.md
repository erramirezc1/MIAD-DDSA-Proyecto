# Modelo de Importaciones

Paquete Python instalable que contiene el modelo de regresión lineal entrenado para predecir el valor CIF de importaciones.

## Instalación

Para instalar el paquete desde el archivo .whl:

```bash
pip install dist/modelo_importaciones-1.0.0-py3-none-any.whl
```

O para construir el paquete desde el código fuente:

```bash
cd modelo_paquete
python setup.py bdist_wheel
pip install dist/modelo_importaciones-1.0.0-py3-none-any.whl
```

## Uso

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

## Parámetros

- `mes`: Mes del año (1-12)
- `pais_pro`: País de origen (ej: "América", "Asia", "Europa", "África", "Oceanía")
- `aduana`: Tipo de aduana ("Maritima y Fluvial" o "Aereas y Terrestres")
- `tipo_importacion`: Tipo de importación (ej: "Importación ordinaria", "Importación con franquicia", etc.)

