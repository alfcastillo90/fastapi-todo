# To-Do List API

API para gestionar una lista de tareas utilizando FastAPI y MySQL.

## Requisitos

- Python 3.8 o superior
- MySQL
- Node.js y npm (para el frontend)

## Instalación

### Backend

1. **Clona el repositorio**:

   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd fastapi-todo
   ```
2. **Crea entorno virtual:**:

   ```bash   
    python3 -m venv env
    source env/bin/activate  # En Windows usa `env\Scripts\activate`
   ```

3. **Instala las dependencias:**:

   ```bash
    pip install fastapi uvicorn sqlalchemy aiomysql pydantic aiosqlite httpx pytest pytest-asyncio
   ```

3. **Inicia el servidor:**:

   ```bash   
    uvicorn app.main:app --reload
   ```