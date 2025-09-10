from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
import models, schemas, crud
from database import SessionLocal, engine, get_db
from typing import List

# Crear tablas (incluye las nuevas)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Productos con Categorías")

# ENDPOINTS PARA CATEGORÍAS

@app.post("/categorias/", response_model=schemas.Categoria)
def crear_categoria(categoria: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    return crud.crear_categoria(db=db, categoria=categoria)

@app.get("/categorias/")
def listar_categorias(db: Session = Depends(get_db)):
    return crud.obtener_categorias(db)

@app.get("/categorias/{categoria_id}", response_model=schemas.CategoriaConProductos)
def obtener_categoria(categoria_id: int, db: Session = Depends(get_db)):
    categoria = crud.obtener_categoria_con_productos(db, categoria_id=categoria_id)
    if categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return categoria

# ENDPOINTS ACTUALIZADOS PARA PRODUCTOS

@app.get("/productos/", response_model=List[schemas.ProductoConCategoria])
def listar_productos_con_categoria(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    return crud.obtener_productos_con_categoria(db, skip=skip, limit=limit)

@app.get("/categorias/{categoria_id}/productos/")
def productos_por_categoria(categoria_id: int, db: Session = Depends(get_db)):
    productos = crud.obtener_productos_por_categoria(db, categoria_id=categoria_id)
    return {
        "categoria_id": categoria_id,
        "productos": productos,
        "total": len(productos)
    }

# ... resto de endpoints existentes ...


# main.py (añadir a tu archivo existente)

# AUTORES
@app.post("/autores/", response_model=schemas.Autor)
def crear_autor(autor: schemas.AutorCreate, db: Session = Depends(get_db)):
    db_autor = models.Autor(**autor.dict())
    db.add(db_autor)
    db.commit()
    db.refresh(db_autor)
    return db_autor

@app.get("/autores/")
def listar_autores(db: Session = Depends(get_db)):
    return db.query(models.Autor).all()

@app.get("/autores/{autor_id}", response_model=schemas.AutorConLibros)
def obtener_autor_con_libros(autor_id: int, db: Session = Depends(get_db)):
    autor = db.query(models.Autor).filter(models.Autor.id == autor_id).first()
    if autor is None:
        raise HTTPException(status_code=404, detail="Autor no encontrado")
    return autor

# LIBROS
@app.post("/libros/", response_model=schemas.LibroConAutor)
def crear_libro(libro: schemas.LibroCreate, db: Session = Depends(get_db)):
    db_libro = models.Libro(**libro.dict())
    db.add(db_libro)
    db.commit()
    db.refresh(db_libro)
    return db_libro

@app.get("/libros/", response_model=List[schemas.LibroConAutor])
def listar_libros_con_autor(db: Session = Depends(get_db)):
    return db.query(models.Libro).all()


# Añadir a main.py
import crud

@app.get("/libros/buscar/")
def buscar_libros(
    titulo: str = Query(None, description="Buscar por título"),
    autor: str = Query(None, description="Buscar por autor"),
    precio_min: float = Query(None, description="Precio mínimo"),
    precio_max: float = Query(None, description="Precio máximo"),
    db: Session = Depends(get_db)
):
    if titulo:
        libros = crud.buscar_libros_por_titulo(db, titulo)
    elif autor:
        libros = crud.buscar_libros_por_autor(db, autor)
    elif precio_min and precio_max:
        libros = crud.obtener_libros_por_precio(db, precio_min, precio_max)
    else:
        libros = db.query(models.Libro).all()

    return {
        "libros": libros,
        "total": len(libros)
    }

@app.get("/estadisticas/")
def estadisticas_libros(db: Session = Depends(get_db)):
    """Estadísticas básicas de la librería"""
    total_libros = db.query(models.Libro).count()
    total_autores = db.query(models.Autor).count()

    if total_libros > 0:
        precios = [libro.precio for libro in db.query(models.Libro).all()]
        precio_promedio = sum(precios) / len(precios)
        precio_max = max(precios)
        precio_min = min(precios)
    else:
        precio_promedio = precio_max = precio_min = 0

    return {
        "total_libros": total_libros,
        "total_autores": total_autores,
        "precio_promedio": precio_promedio,
        "precio_mas_alto": precio_max,
        "precio_mas_bajo": precio_min
    }