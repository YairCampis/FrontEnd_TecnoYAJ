from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from databases import Database
import mysql.connector

app = FastAPI()

# Configuración de la base de datos
DATABASE_URL = "mysql+mysqlconnector://root:@localhost/proyectoscul"
database = Database(DATABASE_URL)

# Modelo de facturacion
class facturacion(BaseModel):
    Id_factura: int
    Id_pago: int
    Fecha_factura:int
    Total_facturado: str


# Crear facturacion
@app.post("/facturacion/")
async def crear_facturacion(facturacion: facturacion):
    query = "INSERT INTO facturacion (facturacion,cc,email,contraseña,telefono,rol) VALUES (:facturacion, :cc, :email, :contraseña, :telefono, :rol)"
    values = {"facturacion": facturacion.facturacion,"cc":facturacion.cc, "email": facturacion.email, "contraseña": facturacion.contraseña,"telefono":facturacion.telefono,"rol":facturacion.rol}
    await database.execute(query=query, values=values)
    return {"message": "facturacion creado exitosamente", "data": facturacion}

# Listar facturacions
@app.get("/facturacion/")
async def listar_facturacion():
    query = "SELECT * FROM facturacion"
    return await database.fetch_all(query=query)

# Obtener facturacion por ID
@app.get("/facturacion/{facturacion_id}/")
async def obtener_facturacion(facturacion_id: int):
    query = "SELECT * FROM facturacion WHERE id = :id"
    values = {"id": facturacion_id}
    facturacion = await database.fetch_one(query=query, values=values)
    if not facturacion:
        raise HTTPException(status_code=404, detail="facturacion no encontrado")
    return {"message": "Detalles del facturacion", "data": facturacion}

# Actualizar facturacion por ID
@app.put("/facturacion/{facturacion_id}/")
async def actualizar_facturacion(facturacion_id: int, facturacion: facturacion):
    query = "UPDATE facturacion SET facturacion = :facturacion, email = :email, contraseña = :contraseña WHERE id = :id"
    values = {"id": facturacion_id, "facturacion": facturacion.facturacion, "email": facturacion.email, "contraseña": facturacion.contraseña}
    await database.execute(query=query, values=values)
    return {"message": "facturacion actualizado exitosamente", "data": facturacion}

# Eliminar facturacion por ID
@app.delete("/facturacion/{facturacion_id}/")
async def eliminar_facturacion(facturacion_id: int):
    query = "DELETE FROM facturacion WHERE id = :id"
    values = {"id": facturacion_id}
    await database.execute(query=query, values=values)
    return {"message": "facturacion eliminado exitosamente", "facturacion_id": facturacion_id}