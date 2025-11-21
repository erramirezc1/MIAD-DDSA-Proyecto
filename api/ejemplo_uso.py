"""
Ejemplo de uso de la API de predicción de importaciones.
"""
import requests
import json

# URL base de la API (ajustar según donde esté corriendo)
BASE_URL = "http://localhost:8000"

def ejemplo_prediccion():
    """Ejemplo de cómo usar el endpoint /predict."""
    print("=" * 60)
    print("Ejemplo de uso del endpoint /predict")
    print("=" * 60)
    
    # Datos de ejemplo
    datos = {
        "mes": 5,
        "pais_pro": "América",
        "aduana": "Maritima y Fluvial",
        "tipo_importacion": "Importación ordinaria"
    }
    
    print(f"\nEnviando solicitud con los siguientes parámetros:")
    print(json.dumps(datos, indent=2, ensure_ascii=False))
    
    try:
        # Realizar petición POST
        response = requests.post(
            f"{BASE_URL}/predict",
            json=datos
        )
        
        # Verificar respuesta
        response.raise_for_status()
        
        # Mostrar resultado
        resultado = response.json()
        print(f"\n✓ Predicción exitosa:")
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
        print(f"\nValor CIF predicho: {resultado['prediccion']:.2f} USD/kg")
        
    except requests.exceptions.RequestException as e:
        print(f"\n✗ Error al realizar la petición: {e}")
        if hasattr(e.response, 'text'):
            print(f"Respuesta del servidor: {e.response.text}")


def ejemplo_info():
    """Ejemplo de cómo obtener información del modelo."""
    print("\n" + "=" * 60)
    print("Ejemplo de uso del endpoint /info")
    print("=" * 60)
    
    try:
        response = requests.get(f"{BASE_URL}/info")
        response.raise_for_status()
        
        info = response.json()
        print("\n✓ Información del modelo:")
        print(json.dumps(info, indent=2, ensure_ascii=False))
        
    except requests.exceptions.RequestException as e:
        print(f"\n✗ Error al obtener información: {e}")


def ejemplo_health():
    """Ejemplo de cómo verificar el estado de la API."""
    print("\n" + "=" * 60)
    print("Ejemplo de uso del endpoint /health")
    print("=" * 60)
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        response.raise_for_status()
        
        health = response.json()
        print("\n✓ Estado de la API:")
        print(json.dumps(health, indent=2, ensure_ascii=False))
        
    except requests.exceptions.RequestException as e:
        print(f"\n✗ Error al verificar estado: {e}")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("EJEMPLOS DE USO DE LA API DE PREDICCIÓN DE IMPORTACIONES")
    print("=" * 60)
    
    # Verificar estado
    ejemplo_health()
    
    # Obtener información
    ejemplo_info()
    
    # Realizar predicción
    ejemplo_prediccion()
    
    print("\n" + "=" * 60)
    print("Ejemplos completados")
    print("=" * 60)

