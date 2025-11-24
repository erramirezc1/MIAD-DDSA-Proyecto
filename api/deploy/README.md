# Manuel de Despliegue API en EC2 Ubuntu

---

Guía rápida para desplegar la API de Predicción de Importaciones en EC2 con Ubuntu.

## Pasos

### 1. Lanzar una instancia en AWS EC2

Lance una instancia en AWS EC2. Se recomienda una máquina t2.small, con sistema operativo
Ubuntu y 20GB de disco. No olvide crear y descargar la `llave.pem`

### 2. Transferir archivos a EC2

Crea las carpetas necesarias en maquina

```bash
ssh -i .\llave.pem ubuntu@tu-ec2-ip "mkdir -p /home/ubuntu/api-importaciones"
```

Desde su equipo con el repositorio clonado, en una terminal puede ejecutar el siguiente comando para cargar los archivos necesario para desplegar el api en la instancia.

```bash
scp -i llave.pem -r api/deploy/ ubuntu@tu-ec2-ip:/home/ubuntu/api-importaciones/
```

### 3. Conectar y ejecutar setup

Desde la misma terminal puede ejecutar el siguiente comando para conectarse a la instancia a través de ssh.

```bash
ssh -i llave.pem ubuntu@tu-ec2-ip
```

Una vez dentro del maquina, debe dirigirse a la ruta donde fueron cargados los archivos.

```bash
cd /home/ubuntu/api-importaciones/deploy
```

Luego, Instalar dos2unix si no está instalado

```bash
sudo apt-get update
sudo apt-get install -y dos2unix

```

a continuacion convertir el archivo

```bash
dos2unix setup-ubuntu.sh
```

Ahora debes darle permisos de ejecución

```bash
chmod +x setup-ubuntu.sh
```

Por ultimo, ejecuta el archivo

```bash
./setup-ubuntu.sh
```

El script configura todo automáticamente:

- Instala dependencias del sistema
- Instala el modelo y dependencias de la API
- Configura firewall (ufw)

### 4. Configurar Security Group en AWS

En la consola de EC2 dentro de la instancia debe ir al `Seguridad > Grupos de seguridad` y luego darle en la opción `editar reglas de entrada`, una vez allí debe agregar una nueva regla con las siguientes características:

- Protocolo: TCP
- Puerto: 8001 (para la API)
- Origen: Anywhere-IPv4 0.0.0.0/0 (o restringir según necesidad)

Y agregar otra regla para la aplicación Dash:
- Protocolo: TCP
- Puerto: 8050 (para la aplicación Dash)
- Origen: Anywhere-IPv4 0.0.0.0/0 (o restringir según necesidad)

## Iniciar la API y la aplicación Dash

El script crea un entorno virtual automáticamente. Para iniciar los servicios:

### Iniciar la API

```bash
# Valide o ingrese a la siguiente ruta
cd /home/ubuntu/api-importaciones/deploy

# Activar el entorno virtual
source venv/bin/activate

# Opción 1: Ejecución directa
uvicorn main:app --host 0.0.0.0 --port 8001

# Opción 2: En segundo plano
nohup uvicorn main:app --host 0.0.0.0 --port 8001 > api.log 2>&1 &
```

### Iniciar la aplicación Dash

```bash
# Asegúrate de estar en el directorio correcto y con el entorno virtual activado
cd /home/ubuntu/api-importaciones/deploy
source venv/bin/activate

# Opción 1: Ejecución directa
python app_dash.py

# Opción 2: En segundo plano
nohup python app_dash.py > dash.log 2>&1 &
```

**Nota:** La aplicación Dash se conecta a la API en `http://localhost:8001` por defecto. Si la API está en otra ubicación, configura la variable de entorno `API_URL` antes de ejecutar:

```bash
export API_URL=http://tu-servidor-api:8001
python app_dash.py
```

## Verificación

```bash
# Verificar que la API funciona
curl http://localhost:8001/health

# Verificar que la aplicación Dash funciona (debe mostrar HTML)
curl http://localhost:8050

# Ver logs (si usas nohup)
tail -f api.log
tail -f dash.log
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
    "pais_pro": "America",
    "aduana": "Maritima y Fluvial",
    "tipo_importacion": "Importación ordinaria"
  }'
```

## Archivos Incluidos

- `main.py` - Aplicación FastAPI
- `app_dash.py` - Aplicación Dash (interfaz web)
- `requirements.txt` - Dependencias
- `modelo_importaciones-1.0.0-py3-none-any.whl` - Modelo entrenado
- `setup-ubuntu.sh` - Script de instalación automática

## Acceso a la Aplicación Dash

Una vez iniciada, la aplicación Dash estará disponible en:
- `http://tu-ec2-ip:8050`

La aplicación permite ingresar parámetros de importación (mes, país de origen, aduana, tipo de importación) y obtener predicciones del valor CIF de forma interactiva.

