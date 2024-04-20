from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from databases import Database
import mysql.connector

app = FastAPI()

# Configuración de la base de datos
DATABASE_URL = "mysql+mysqlconnector://root:@localhost/proyectoscul"
database = Database(DATABASE_URL)

# Modelo de pago
class pago(BaseModel):
    Id_pago: int
    pago: str
    cc:int
    email: str
    contraseña: str
    telefono:int
    rol:str


# Crear pago
@app.post("/pagos/")
async def crear_pago(pago: pago):
    query = "INSERT INTO pagos (pago,cc,email,contraseña,telefono,rol) VALUES (:pago, :cc, :email, :contraseña, :telefono, :rol)"
    values = {"pago": pago.pago,"cc":pago.cc, "email": pago.email, "contraseña": pago.contraseña,"telefono":pago.telefono,"rol":pago.rol}
    await database.execute(query=query, values=values)
    return {"message": "pago creado exitosamente", "data": pago}

# Listar pagos
@app.get("/pagos/")
async def listar_pagos():
    query = "SELECT * FROM pagos"
    return await database.fetch_all(query=query)

# Obtener pago por ID
@app.get("/pagos/{pago_id}/")
async def obtener_pago(pago_id: int):
    query = "SELECT * FROM pagos WHERE id = :id"
    values = {"id": pago_id}
    pago = await database.fetch_one(query=query, values=values)
    if not pago:
        raise HTTPException(status_code=404, detail="pago no encontrado")
    return {"message": "Detalles del pago", "data": pago}

# Actualizar pago por ID
@app.put("/pagos/{pago_id}/")
async def actualizar_pago(pago_id: int, pago: pago):
    query = "UPDATE pagos SET pago = :pago, email = :email, contraseña = :contraseña WHERE id = :id"
    values = {"id": pago_id, "pago": pago.pago, "email": pago.email, "contraseña": pago.contraseña}
    await database.execute(query=query, values=values)
    return {"message": "pago actualizado exitosamente", "data": pago}

# Eliminar pago por ID
@app.delete("/pagos/{pago_id}/")
async def eliminar_pago(pago_id: int):
    query = "DELETE FROM pagos WHERE id = :id"
    values = {"id": pago_id}
    await database.execute(query=query, values=values)
    return {"message": "pago eliminado exitosamente", "pago_id": pago_id}