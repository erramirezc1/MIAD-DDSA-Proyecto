"""
API FastAPI para predecir valor CIF de importaciones usando el modelo empaquetado.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from modelo_importaciones import ModeloImportaciones

# Crear instancia de FastAPI
app = FastAPI(
    title="API de Predicción de Importaciones",
    description="API para predecir el valor CIF de importaciones usando modelo de regresión lineal",
    version="1.0.0"
)

# Cargar el modelo al iniciar la aplicación
try:
    modelo = ModeloImportaciones()
    info_modelo = modelo.obtener_info()
except Exception as e:
    raise RuntimeError(f"Error al cargar el modelo: {e}") from e


# Modelos Pydantic para validación de entrada
class PrediccionRequest(BaseModel):
    """Modelo de datos para la solicitud de predicción."""
    mes: int = Field(..., ge=1, le=12, description="Mes del año (1-12)")
    pais_pro: str = Field(..., description="País de origen (ej: América, Asia, Europa, África, Oceanía)")
    aduana: str = Field(..., description="Tipo de aduana: 'Maritima y Fluvial' o 'Aereas y Terrestres'")
    tipo_importacion: str = Field(..., description="Tipo de importación (ej: Importación ordinaria)")

    class Config:
        schema_extra = {
            "example": {
                "mes": 5,
                "pais_pro": "América",
                "aduana": "Maritima y Fluvial",
                "tipo_importacion": "Importación ordinaria"
            }
        }


class PrediccionResponse(BaseModel):
    """Modelo de datos para la respuesta de predicción."""
    prediccion: float = Field(..., description="Valor CIF predicho en USD/kg")
    mes: int
    pais_pro: str
    aduana: str
    tipo_importacion: str


class InfoResponse(BaseModel):
    """Información sobre el modelo y categorías disponibles."""
    paises_disponibles: list[str]
    aduanas_disponibles: list[str]
    tipos_disponibles: list[str]
    metricas: dict


@app.get("/")
async def root():
    """Endpoint raíz con información de la API."""
    return {
        "mensaje": "API de Predicción de Importaciones",
        "version": "1.0.0",
        "endpoints": {
            "/predict": "POST - Realizar predicción de valor CIF",
            "/info": "GET - Obtener información del modelo",
            "/health": "GET - Verificar estado de la API"
        }
    }


@app.get("/health")
async def health_check():
    """Endpoint para verificar el estado de la API."""
    return {
        "status": "healthy",
        "modelo_cargado": modelo is not None
    }


@app.get("/info", response_model=InfoResponse)
async def obtener_info():
    """Obtiene información sobre el modelo y las categorías disponibles."""
    try:
        info = modelo.obtener_info()
        return InfoResponse(
            paises_disponibles=info.get("paises", []),
            aduanas_disponibles=info.get("aduanas", []),
            tipos_disponibles=info.get("tipos", []),
            metricas=info.get("metricas", {})
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener información: {str(e)}")


@app.post("/predict", response_model=PrediccionResponse)
async def predecir(request: PrediccionRequest):
    """
    Realiza una predicción del valor CIF usando el modelo entrenado.
    
    Recibe 4 parámetros:
    - mes: Mes del año (1-12)
    - pais_pro: País de origen
    - aduana: Tipo de aduana
    - tipo_importacion: Tipo de importación
    
    Retorna la predicción del valor CIF en USD/kg.
    """
    try:
        # Realizar predicción
        prediccion = modelo.predecir(
            mes=request.mes,
            pais_pro=request.pais_pro,
            aduana=request.aduana,
            tipo_importacion=request.tipo_importacion
        )
        
        return PrediccionResponse(
            prediccion=prediccion,
            mes=request.mes,
            pais_pro=request.pais_pro,
            aduana=request.aduana,
            tipo_importacion=request.tipo_importacion
        )
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al realizar predicción: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

