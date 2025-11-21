#!/bin/bash
# Script completo de setup para Ubuntu EC2
# Este script hace todo: instalación y firewall

set -e

echo "=========================================="
echo "Setup Completo para Ubuntu EC2"
echo "API de Predicción de Importaciones"
echo "=========================================="

# Verificar que es Ubuntu
if [ ! -f /etc/os-release ]; then
    echo "ERROR: No se pudo detectar el sistema operativo"
    exit 1
fi

. /etc/os-release
if [ "$ID" != "ubuntu" ]; then
    echo "ADVERTENCIA: Este script está optimizado para Ubuntu"
    read -p "¿Continuar de todos modos? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Paso 1: Instalación
echo ""
echo "=========================================="
echo "Paso 1: Instalando dependencias"
echo "=========================================="

# Actualizar sistema
echo "Actualizando lista de paquetes..."
sudo apt-get update -qq

echo "Instalando dependencias del sistema..."
sudo apt-get install -y python3 python3-pip python3-venv curl python3-full

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 no está instalado"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "Python detectado: $PYTHON_VERSION"

# Crear entorno virtual
echo ""
echo "Creando entorno virtual..."
if [ -d "venv" ]; then
    echo "El entorno virtual ya existe, eliminándolo..."
    rm -rf venv
fi

python3 -m venv venv

# Activar entorno virtual
echo "Activando entorno virtual..."
source venv/bin/activate

# Actualizar pip
echo "Actualizando pip..."
pip install --upgrade pip --quiet

# Instalar el paquete del modelo
echo ""
echo "Instalando paquete del modelo..."
if [ ! -f "modelo_importaciones-1.0.0-py3-none-any.whl" ]; then
    echo "ERROR: No se encontró el archivo modelo_importaciones-1.0.0-py3-none-any.whl"
    exit 1
fi

pip install --quiet modelo_importaciones-1.0.0-py3-none-any.whl

# Instalar dependencias de la API
echo "Instalando dependencias de la API..."
pip install --quiet -r requirements.txt

# Verificar instalación
echo "Verificando instalación..."
python -c "from modelo_importaciones import ModeloImportaciones; m = ModeloImportaciones(); print('Modelo cargado correctamente')" || {
    echo "ERROR: No se pudo cargar el modelo"
    exit 1
}

# Paso 2: Configurar firewall
echo ""
echo "=========================================="
echo "Paso 2: Configurando firewall (ufw)"
echo "=========================================="

if command -v ufw &> /dev/null; then
    echo "Configurando reglas de firewall..."
    sudo ufw allow 8001/tcp comment "API Importaciones"
    echo "Puerto 8001 abierto en firewall"
    
    # Verificar estado
    echo ""
    echo "Estado del firewall:"
    sudo ufw status
else
    echo "ADVERTENCIA: ufw no está instalado. El firewall puede estar deshabilitado."
fi

# Paso 3: Verificación
echo ""
echo "=========================================="
echo "Paso 3: Verificación"
echo "=========================================="

echo ""
echo "NOTA: La verificación del endpoint requiere que la API esté corriendo."
echo "      Para iniciar la API, activa el entorno virtual y ejecuta:"
echo "      source venv/bin/activate"
echo "      uvicorn main:app --host 0.0.0.0 --port 8001"

echo ""
echo "=========================================="
echo "Setup completado"
echo "=========================================="
echo ""
echo "La API debería estar disponible en:"
echo "  http://$(curl -s ifconfig.me):8001"
echo ""
echo "Documentación interactiva:"
echo "  http://$(curl -s ifconfig.me):8001/docs"
echo ""
echo "Recuerda configurar el Security Group de EC2 para permitir tráfico en el puerto 8001"
echo ""
echo "Para iniciar la API, ejecuta:"
echo "  source venv/bin/activate"
echo "  uvicorn main:app --host 0.0.0.0 --port 8001"
echo ""
echo "O en segundo plano:"
echo "  source venv/bin/activate"
echo "  nohup uvicorn main:app --host 0.0.0.0 --port 8001 > api.log 2>&1 &"
echo ""
echo "NOTA: El entorno virtual se creó en ./venv"
echo "      Siempre activa el entorno virtual antes de ejecutar la API"
echo ""

