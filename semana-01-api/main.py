from fastapi import FastAPI

app = FastAPI(title="Mi Primera API")

@app.get("/")
def hello_world():
    return {"message": "¡Mi primera API FastAPI!"}

@app.get("/info")
def info():
    return {"api": "FastAPI", "week": 1, "status": "running"}

# NUEVO: Endpoint personalizado (solo si hay tiempo)
@app.get("/greeting/{name}")
def greet_user(name: str):
    return {"greeting": f"¡Hola {name}!"}

# Agregar al final de tu main.py existente

@app.get("/my-profile")
def my_profile():
    return {
        "name": "Valery",           # Cambiar por tu nombre
        "bootcamp": "FastAPI",
        "week": 1,
        "date": "2025",
        "likes_fastapi": True              # ¿Te gustó FastAPI?
    }
    