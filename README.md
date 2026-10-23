# API de gestión de aprendices

Proyecto FastAPI para registrar, consultar, actualizar y eliminar aprendices en MongoDB. Incluye una interfaz de consola (`src/views/view.py`) para consumir la API.

## 1. Abrir la carpeta correcta

Al descomprimir el ZIP, abre en VS Code la carpeta **`tll_fastapi`**, que contiene `requirements.txt` y la carpeta `src`. Si la terminal está en la carpeta exterior, entra a la carpeta del proyecto:

```powershell
cd .\tll_fastapi
```

Si ya estás dentro de `tll_fastapi`, no ejecutes ese `cd` otra vez.

## 2. Instalar dependencias (Windows / PowerShell)

```powershell
py -m pip install -r requirements.txt
```

Si `py` no funciona pero `python` sí, usa `python -m pip install -r requirements.txt`.

## 3. Configurar MongoDB

El archivo `.env` se incluye con una URI local de ejemplo para evitar exponer contraseñas. Para usar MongoDB Atlas, reemplaza el valor de `MONGO_URL` en `.env` por tu URI real. No compartas el archivo `.env`.

La API puede iniciar aunque MongoDB no esté disponible; las operaciones de aprendices devolverán HTTP 503 hasta que configures una base de datos accesible.

## 4. Iniciar la API

Desde la raíz `tll_fastapi` (la carpeta que contiene `src`), ejecuta:

```powershell
py -m uvicorn src.main:app --reload
```

Si `py` no funciona, prueba `python -m uvicorn src.main:app --reload`. Deja abierta esa terminal mientras uses la API.

Abre en el navegador:

- API: <http://127.0.0.1:8000>
- Documentación interactiva: <http://127.0.0.1:8000/docs>
- Documentación alternativa: <http://127.0.0.1:8000/redoc>

Si el navegador muestra `ERR_CONNECTION_REFUSED`, el servidor no está ejecutándose o no inició correctamente. Revisa el error de la terminal y no cierres la ventana del servidor.

## 5. Interfaz de consola solicitada

Con la API funcionando, abre una **segunda terminal** en la misma raíz `tll_fastapi` y ejecuta:

```powershell
py -m src.views.view
```

Alternativa: `python -m src.views.view`. El menú permite registrar, listar, consultar, actualizar y eliminar aprendices a través de las rutas HTTP.

## Rutas de la API

| Método | Ruta | Función |
|---|---|---|
| GET | `/` | Verificar que la API responde |
| POST | `/Trainees/` | Registrar aprendiz |
| GET | `/Trainees/` | Listar aprendices |
| GET | `/Trainees/{id}` | Consultar por ID |
| PUT | `/Trainees/{id}` | Actualizar por ID |
| DELETE | `/Trainees/{id}` | Eliminar por ID |

## Solución de problemas

- `py` no reconocido: prueba `python --version`. Si ambos fallan, instala Python y activa la opción para agregarlo al PATH.
- `No module named uvicorn`: ejecuta `py -m pip install -r requirements.txt`.
- `No module named src`: estás en la carpeta incorrecta; cambia a `tll_fastapi`, donde están `requirements.txt` y `src`.
- `ERR_CONNECTION_REFUSED`: inicia el servidor y deja la terminal abierta.
- HTTP 503 al usar aprendices: verifica la URI en `.env`, el acceso de red y las credenciales de MongoDB Atlas.

**Seguridad:** la versión anterior del proyecto contenía una URI con contraseña escrita directamente en el código. Si esa contraseña es real, cámbiala en MongoDB Atlas y usa la nueva URI únicamente en tu archivo local `.env`.
