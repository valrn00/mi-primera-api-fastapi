
cat > README.md << EOF
# Mi Primera API FastAPI - Bootcamp

**��� Desarrollador**: Valery
**��� Email**: 199391218+valrn00@users.noreply.github.com.
**� Privacidad**: Email configurado según mejores prácticas de GitHub
**���� Fecha de creación**: 2025-08-02 16:43:02
**��� Ruta del proyecto**: /c/Users/Aprendiz/desarrollo-personal/valery-gaona-bootcamp/mi-primera-api-fastapi
**��� Equipo de trabajo**: BOGDFPCGMP5693

## ��� Configuración Local

Este proyecto está configurado para trabajo en equipo compartido:

- **Entorno virtual aislado**: `venv-personal/`
- **Configuración Git local**: Solo para este proyecto
- **Dependencias independientes**: No afecta otras instalaciones

## ��� Instalación y Ejecución

```bash
# 1. Activar entorno virtual personal
source venv-personal/bin/activate

# 2. Instalar dependencias (si es necesario)
pip install -r requirements.txt

# 3. Ejecutar servidor de desarrollo
uvicorn main:app --reload --port 8000
```

## ��� Notas del Desarrollador

- **Configuración Git**: Local únicamente, no afecta configuración global
- **Email de GitHub**: Configurado con email privado para proteger información personal
- **Entorno aislado**: Todas las dependencias en venv-personal/
- **Puerto por defecto**: 8000 (cambiar si hay conflictos)
- **Estado del bootcamp**: Semana 1 - Configuración inicial

## ���️ Troubleshooting Personal

- Si el entorno virtual no se activa: `rm -rf venv-personal && python3 -m venv venv-personal`
- Si hay conflictos de puerto: cambiar --port en uvicorn
- Si Git no funciona: verificar `git config user.name` y `git config user.email`
- Si necesitas cambiar el email: usar el email privado de GitHub desde Settings → Emails
# Mi Primera API FastAPI - Bootcamp

**��� Desarrollador**: Valery
**��� Email**: 199391218+valrn00@users.noreply.github.com.
**� Privacidad**: Email configurado según mejores prácticas de GitHub
**���� Fecha de creación**: 2025-08-02 16:43:02
**��� Ruta del proyecto**: /c/Users/Aprendiz/desarrollo-personal/valery-gaona-bootcamp/mi-primera-api-fastapi
**��� Equipo de trabajo**: BOGDFPCGMP5693

## ��� Configuración Local

Este proyecto está configurado para trabajo en equipo compartido:

- **Entorno virtual aislado**: `venv-personal/`
- **Configuración Git local**: Solo para este proyecto
- **Dependencias independientes**: No afecta otras instalaciones

## ��� Instalación y Ejecución

```bash
# 1. Activar entorno virtual personal
source venv-personal/bin/activate

# 2. Instalar dependencias (si es necesario)
pip install -r requirements.txt

# 3. Ejecutar servidor de desarrollo
uvicorn main:app --reload --port 8000
```

## ��� Notas del Desarrollador

- **Configuración Git**: Local únicamente, no afecta configuración global
- **Email de GitHub**: Configurado con email privado para proteger información personal
- **Entorno aislado**: Todas las dependencias en venv-personal/
- **Puerto por defecto**: 8000 (cambiar si hay conflictos)
- **Estado del bootcamp**: Semana 1 - Configuración inicial

## ���️ Troubleshooting Personal

- Si el entorno virtual no se activa: `rm -rf venv-personal && python3 -m venv venv-personal`
- Si hay conflictos de puerto: cambiar --port en uvicorn
- Si Git no funciona: verificar `git config user.name` y `git config user.email`
- Si necesitas cambiar el email: usar el email privado de GitHub desde Settings → Emails

# Mi API FastAPI - Semana 2

## ¿Qué hace?

API mejorada con validación automática de datos y type hints.

## Nuevos Features (Semana 2)

- ✅ Type hints en todas las funciones
- ✅ Validación automática con Pydantic
- ✅ Endpoint POST para crear datos
- ✅ Parámetros de ruta (ejemplo: /products/{id})
- ✅ Búsqueda con parámetros query

## ¿Cómo ejecutar?

```bash
pip install fastapi pydantic uvicorn
uvicorn main:app --reload
```
````

## Endpoints principales

- `GET /`: Mensaje de bienvenida
- `POST /products`: Crear nuevo producto
- `GET /products`: Ver todos los productos
- `GET /products/{id}`: Ver producto específico
- `GET /search?name=...`: Buscar productos

## Documentación

http://127.0.0.1:8000/docs

## Mi progreso

**Semana 1**: API básica con Hello World
**Semana 2**: API con validación y type hints

## Reflexión
Lo más útil de esta semana fue aprender a usar Pydantic y los parámetros de ruta y query. Estos elementos no solo validan los datos de entrada, sino que también permiten la creación de endpoints más dinámicos y funcionales, como la búsqueda y el filtrado de productos, que son esenciales en cualquier aplicación del mundo real.

**¿Los type hints hacen tu código más claro? ¿Por qué?**
Al indicar el tipo de dato esperado para los parámetros de las funciones, el tipo de dato que devuelven y mejoran la legibilidad

**¿Cómo te ayuda Pydantic a crear APIs más robustas?**
Pydantic ayuda a crear APIs más robustas al proporcionar validación automática de datos. Esto asegura que la información recibida en los endpoints POST, por ejemplo, cumpla con la estructura y el tipo de dato definidos

**¿Cómo mejoraron estos conceptos tu API comparada con Semana 1?**
Estos conceptos mejoraron significativamente la API al transformarla de una colección de endpoints simples a una aplicación web más profesional y confiable. La validación con Pydantic y los type hints garantizan que los datos sean correctos, mientras que los parámetros de ruta y query permiten una interacción con el usuario más compleja y flexible

