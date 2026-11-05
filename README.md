# Ficha de Duke

Sitio web de la ficha de una mascota con frontend estático y backend en
Python. Los datos de dueños y mascotas se guardan en MySQL.

## Estructura

```text
.
├── backend/
│   ├── sql/
│   │   ├── esquema.sql        # Creación de la base y las tablas
│   │   ├── migracion_qr_mascotas.sql # Almacenamiento de rutas QR
│   │   ├── datos_ejemplo.sql  # Dueño, mascota, fotos y eventos de ejemplo
│   │   └── datos_prueba.sql   # 4 dueños y 6 mascotas ficticias de prueba
│   ├── .env.example           # Plantilla de configuración de MySQL
│   ├── requirements.txt
│   ├── server.py              # Punto de entrada Flask
│   └── ficha_app/
│       ├── __init__.py        # Fábrica de la aplicación
│       ├── config.py          # Variables de entorno
│       ├── database.py        # Conexión a MySQL
│       ├── repository.py      # Consultas y persistencia
│       ├── serializers.py     # Conversión de filas a JSON
│       ├── qr.py              # Generación de códigos QR
│       └── routes.py          # Rutas web y API
├── frontend/
│   ├── public/
│   ├── ficha.html
│   ├── datos.js
│   ├── index.html
│   ├── selector-mascotas.js
│   ├── mascota.html
│   ├── script.js
│   └── styles.css
├── .gitignore
├── README.md
└── Consignas Primer Examen Parcial.pdf
```

El backend está dividido por responsabilidad: `server.py` inicia el servidor,
`ficha_app/routes.py` declara las rutas y los módulos restantes manejan
configuración, base de datos, serialización, consultas y QR.

## Base de datos

La base se llama `ficha_mascotas` y tiene estas tablas:

| Tabla | Contenido |
|---|---|
| `duenos` | Datos personales y redes del dueño |
| `mascotas` | Datos de cada mascota y su dueño |
| `mascota_fotos` | Galería de fotos de cada mascota |
| `mascota_eventos_medicos` | Historial médico de cada mascota |

La relación es **uno a muchos**: `mascotas.dueno_id` referencia a `duenos.id`
mediante una clave foránea, así que un dueño puede tener varias mascotas.

También existe la vista `vista_duenos_mascotas`, que devuelve la relación ya
resuelta para consultas rápidas.

### Crear la base

Desde la raíz del proyecto:

```powershell
mysql -u root -p --default-character-set=utf8mb4 -e "source backend/sql/esquema.sql"
mysql -u root -p --default-character-set=utf8mb4 -e "source backend/sql/datos_ejemplo.sql"
mysql -u root -p --default-character-set=utf8mb4 -e "source backend/sql/datos_prueba.sql"
```

`datos_prueba.sql` agrega 4 dueños ficticios (IDs 2 a 5) y 6 mascotas
ficticias (IDs 2 a 7), con fotos genéricas y algunos eventos médicos. En total
quedan 5 dueños y 7 mascotas contando el ejemplo original de Duke.

Si `mysql` no está en el PATH, usá la ruta completa, por ejemplo:

```powershell
& 'C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe' -u root -p --default-character-set=utf8mb4 -e "source backend/sql/esquema.sql"
```

Si la base ya existía antes de agregar el almacenamiento de QR, aplicá la
migración una sola vez desde la raíz del proyecto:

```powershell
mysql -u root -p --default-character-set=utf8mb4 -e "source backend/sql/migracion_qr_mascotas.sql"
```

La migración crea `mascota_qr`, donde se guarda la ruta relativa de la ficha
asociada a cada mascota. El QR se regenera con el host actual al solicitarlo,
así que no se persiste una IP que pueda cambiar al pasar a otra red.

## Configuración del backend

Copiá `backend/.env.example` a `backend/.env` y completá la contraseña:

```text
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=tu_contraseña
MYSQL_DB=ficha_mascotas
APP_PORT=8000
```

El archivo `backend/.env` está excluido de Git.

## Ejecución

```powershell
pip install -r backend/requirements.txt
python backend/server.py
```

Luego abrir <http://127.0.0.1:8000> para ver el selector de mascotas.

Para usar otro puerto:

```powershell
python backend/server.py --puerto 8080
```

También se puede establecer el puerto predeterminado con `APP_PORT` en
`backend/.env`. El servidor Flask de desarrollo escucha por defecto en
`0.0.0.0`, por lo que también acepta conexiones desde otros dispositivos de la
red local.

## Instalación en otra PC

Hay dos formas de usarlo en otra computadora.

### Opción A: instalar todo en la otra PC

Requisitos:

- Python 3.10 o superior. Al instalarlo, marcar **Add Python to PATH**.
- MySQL Server 8. Anotar la contraseña del usuario `root`.
- Git, solo si se va a clonar el repositorio.

1. Copiar la carpeta del proyecto a la otra PC (por ejemplo, por USB o red) o
   clonar el repositorio. No hace falta copiar `backend/.env` ni
   `__pycache__/`.

2. Instalar las dependencias desde la raíz del proyecto:

```powershell
python -m pip install -r backend/requirements.txt
```

3. Crear la base y cargar los datos:

```powershell
mysql -u root -p --default-character-set=utf8mb4 -e "source backend/sql/esquema.sql"
mysql -u root -p --default-character-set=utf8mb4 -e "source backend/sql/datos_ejemplo.sql"
mysql -u root -p --default-character-set=utf8mb4 -e "source backend/sql/datos_prueba.sql"
```

Si `mysql` no está en el PATH, usar la ruta completa, por ejemplo
`& 'C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe' ...`.

4. Crear `backend/.env` a partir de la plantilla y escribir la contraseña de
   MySQL de esa PC:

```powershell
Copy-Item backend/.env.example backend/.env
notepad backend/.env
```

El archivo debe quedar así, con la contraseña local:

```text
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=la_contraseña_de_esa_pc
MYSQL_DB=ficha_mascotas
APP_PORT=8000
```

5. Iniciar el servidor:

```powershell
python backend/server.py
```

6. Abrir <http://127.0.0.1:8000> en esa PC para ver el selector de mascotas.

`backend/.env` está excluido de Git, así que no se copia con el repositorio:
hay que crearlo en cada PC. La contraseña de MySQL puede ser distinta en cada
una.

En macOS o Linux los comandos son los mismos, reemplazando `python` por
`python3` y `Copy-Item` por `cp`.

### Opción B: usarla desde otra PC sin instalar nada

La base y el servidor quedan en la PC original; la otra solo abre el
navegador.

1. En la PC que tiene el proyecto, iniciar el servidor. Por defecto acepta
   conexiones de la red local; también se puede indicar el host explícitamente:

```powershell
python backend/server.py --host 0.0.0.0
```

2. Averiguar la IP local de esa PC:

```powershell
ipconfig
```

Buscar la **Dirección IPv4** de la conexión activa, por ejemplo
`192.168.0.15`.

3. Desde la otra PC, abrir en el navegador:

```text
http://192.168.0.15:8000/?id=3
```

Cambiando el ID se ven las demás mascotas. La URL `127.0.0.1` solo funciona en
la misma computadora donde corre el servidor.

Si no carga, revisar:

- Que las dos PCs estén en la misma red (Wi-Fi o cable).
- Que la PC del servidor esté encendida y el servidor siga corriendo.
- Permitir Python o el puerto 8000 en el Firewall de Windows. Desde
  PowerShell como administrador:

```powershell
New-NetFirewallRule -DisplayName "Ficha mascotas 8000" -Direction Inbound -Protocol TCP -LocalPort 8000 -Action Allow
```

MySQL solo necesita estar instalado en la PC que ejecuta el backend. La otra
PC únicamente usa el navegador.

## Ver una mascota

La página principal muestra las mascotas disponibles en un selector. Al elegir
una, aparece un QR que abre su ficha en el mismo servidor. La ficha individual
también muestra un QR para abrir esa misma ficha y se puede abrir directamente
según su ID:

```text
http://127.0.0.1:8000/ficha.html?id=3
```

Ese ejemplo muestra a **Rocky** (ID 3). Si no se indica `id`, se muestra la
mascota 1 (Duke). Las URLs anteriores `/?id=<id>` siguen redirigiendo a la
ficha correspondiente. Para ver otra mascota, cambiá el ID:

| URL | Mascota |
|---|---|
| `/ficha.html?id=1` | Duke |
| `/ficha.html?id=2` | Luna |
| `/ficha.html?id=3` | Rocky |
| `/ficha.html?id=4` | Milo |
| `/ficha.html?id=5` | Nina |
| `/ficha.html?id=6` | Simba |
| `/ficha.html?id=7` | Coco |

Si el ID no existe, la página muestra un mensaje de error.

## Endpoints

| Ruta | Descripción |
|---|---|
| `/` | Sitio web |
| `/api/dueno` | Primer dueño (usado por el frontend) |
| `/api/duenos` | Dueños con sus mascotas y `total_mascotas` |
| `/api/duenos/<id>` | Dueño con sus mascotas |
| `/api/duenos/<id>/mascotas` | Mascotas de un dueño |
| `/api/mascotas` | Listado de mascotas |
| `/api/mascotas?dueno_id=<id>` | Mascotas filtradas por dueño |
| `/api/mascotas/<id>` | Mascota con dueño, fotos y eventos médicos |
| `/api/qr?dueno_id=<id>` | QR en SVG con los datos del dueño |
| `/api/qr/mascota/<id>` | QR en SVG con la URL de la ficha de la mascota |
