# 🎬 Movie Reservation API

API REST desarrollada con **FastAPI** para gestionar un sistema de reservas de funciones de cine. Permite la creación y gestión de películas, auditorios (con asientos), funciones, y reservas de asientos para funciones específicas. Utiliza **SQLite** como base de datos para la persistencia de datos.

# 🚀 Características

- Crear, listar, actualizar y eliminar **películas**
- Crear y administrar **auditorios** con cantidad de asientos
- Programar **funciones** (película + horario + auditorio)
- Realizar **reservas** para funciones, seleccionando asientos disponibles

# 🛠 Tecnologías utilizadas

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLite](https://www.sqlite.org/index.html)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pydantic](https://docs.pydantic.dev/)
- [Uvicorn](https://www.uvicorn.org/) - servidor ASGI
- [Pytest](https://docs.pytest.org/) - para pruebas automatizadas

# 📦 Instalación

1. Clona este repositorio:

```
git clone https://github.com/tu_usuario/movie_reservation.git
cd movie_reservation```

2. Crea y activa un entorno virtual:
```python -m venv venv
source venv/bin/activate   # En Windows: venv\Scripts\activate```

3. Instala las dependencias:
```pip install -r requirements.txt```

4. Ejecuta la aplicación:
```uvicorn main:app --reload```

# 📚 Documentación interactiva

Una vez ejecutado el servidor, podés acceder a la documentación automática generada por FastAPI:
Swagger UI: http://127.0.0.1:8000/docs

# 🧪 Ejecutar tests

El proyecto incluye pruebas automatizadas con pytest. Para ejecutarlas, usá el siguiente comando:
```pytest```

# Contacto
  www.linkedin.com/in/ta-cardozo
