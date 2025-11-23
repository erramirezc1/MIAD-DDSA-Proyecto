# Despliegue en EC2 Ubuntu

Guía rápida para desplegar la API de Predicción de Importaciones en EC2 con Ubuntu.

## Pasos:

### 0. Crear instancia EC2 en la consola de AWS

Lance una instancia en AWS EC2. Se recomienda una máquina t2.small, con sistema operativo
Ubuntu y 20GB de disco. No olvide crear y descargar su `llave.pem`

### 1. Transferir archivos a EC2

```bash
scp -i llave.pem -r api/deploy_api/ ubuntu@tu-ec2-ip:/home/ubuntu/api-importaciones/
```

### 2. Conectar y ejecutar setup

```bash
ssh -i llave.pem ubuntu@tu-ec2-ip
cd /home/ubuntu/api-importaciones
chmod +x setup-ubuntu.sh
./setup-ubuntu.sh
```

El script configura todo automáticamente:

- Instala dependencias del sistema
- Instala el modelo y dependencias de la API
- Configura firewall (ufw)

### 3. Configurar Security Group en AWS

En la consola de EC2:

- Puerto: 8001
- Protocolo: TCP
- Origen: 0.0.0.0/0 (o restringir según necesidad)

## Iniciar la API

El script crea un entorno virtual automáticamente. Para iniciar la API:

```bash
# Activar el entorno virtual
source venv/bin/activate

# Opción 1: Ejecución directa
uvicorn main:app --host 0.0.0.0 --port 8001

# Opción 2: En segundo plano
nohup uvicorn main:app --host 0.0.0.0 --port 8001 > api.log 2>&1 &
```

## Verificación

```bash
# Verificar que la API funciona
curl http://localhost:8001/health

# Ver logs (si usas nohup)
tail -f api.log
```

## Endpoints

- `GET /` - Información de la API
- `GET /health` - Estado de la API
- `GET /info` - Información del modelo
- `POST /predict` - Realizar predicción
- `GET /docs` - Documentación interactiva (Swagger)

## Ejemplo de Uso

```bash
curl -X POST "http://tu-ec2-ip:8001/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "mes": 5,
    "pais_pro": "América",
    "aduana": "Maritima y Fluvial",
    "tipo_importacion": "Importación ordinaria"
  }'
```

## Archivos Incluidos

- `main.py` - Aplicación FastAPI
- `requirements.txt` - Dependencias
- `modelo_importaciones-1.0.0-py3-none-any.whl` - Modelo entrenado
- `setup-ubuntu.sh` - Script de instalación automática

## Notas

- El modelo NO se reentrena, solo se carga desde el paquete
- Optimizado para Ubuntu 20.04+ en EC2
- Usa entorno virtual (venv) para evitar conflictos con el sistema
- Listo para producción

