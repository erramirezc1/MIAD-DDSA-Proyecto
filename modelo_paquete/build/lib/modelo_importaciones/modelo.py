"""
Módulo para cargar y usar el modelo de regresión lineal entrenado.
"""
import joblib
import numpy as np
import pandas as pd
from pathlib import Path

class ModeloImportaciones:
    """Clase para cargar y usar el modelo de regresión lineal entrenado."""
    
    def __init__(self):
        """Inicializa el modelo cargándolo desde el archivo guardado."""
        # Obtener la ruta del modelo relativa al paquete
        package_dir = Path(__file__).resolve().parent
        model_path = package_dir / "model" / "modelo_regresion_lineal.pkl"
        info_path = package_dir / "model" / "modelo_info.pkl"
        
        if not model_path.exists():
            raise FileNotFoundError(
                f"No se encontró el modelo en {model_path}. "
                "Asegúrate de haber ejecutado train_model.py primero."
            )
        
        # Cargar modelo e información
        self.modelo = joblib.load(model_path)
        self.info = joblib.load(info_path) if info_path.exists() else {}
    
    def predecir(self, mes: int, pais_pro: str, aduana: str, tipo_importacion: str) -> float:
        """
        Realiza una predicción del valor CIF usando el modelo entrenado.
        
        Args:
            mes: Mes del año (1-12)
            pais_pro: País de origen (ej: "América", "Asia", "Europa", etc.)
            aduana: Tipo de aduana ("Maritima y Fluvial" o "Aereas y Terrestres")
            tipo_importacion: Tipo de importación (ej: "Importación ordinaria", etc.)
        
        Returns:
            Predicción del valor CIF en USD/kg
        """
        # Validar mes
        if not (1 <= mes <= 12):
            raise ValueError("El mes debe estar entre 1 y 12")
        
        # Crear transformaciones cíclicas del mes
        sin_fech = np.sin(2 * np.pi * mes / 12)
        cos_fech = np.cos(2 * np.pi * mes / 12)
        
        # Crear DataFrame con los datos de entrada
        datos = pd.DataFrame({
            'fech': [mes],
            'sin_fech': [sin_fech],
            'cos_fech': [cos_fech],
            'adua': [aduana],
            'paispro': [pais_pro],
            'tipoim': [tipo_importacion]
        })
        
        # Realizar predicción
        prediccion = self.modelo.predict(datos)[0]
        
        return float(prediccion)
    
    def obtener_info(self) -> dict:
        """Retorna información sobre el modelo y las categorías disponibles."""
        return self.info.copy()

