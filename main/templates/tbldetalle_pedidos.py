from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from databases import Database
import mysql.connector

app = FastAPI()

# Configuración de la base de datos
DATABASE_URL = "mysql+mysqlconnector://root:@localhost/proyectoscul"
database = Database(DATABASE_URL)

# Modelo de detalle_pedidos
class detalle_pedidos(BaseModel):
    Id_detalle_pedido: int
    Id_pedido: int
    Id_producto:int
    Cantidad: int
    Precio_unitario: str


# Crear detalle_pedidos
@app.post("/detalle_pedidos/")
async def crear_detalle_pedidos(detalle_pedidos: detalle_pedidos):
    query = "INSERT INTO detalle_pedidos (Id_pedido,Id_producto,Cantidad,Precio_unitario) VALUES (:Id_pedido, :Id_producto, :Cantidad, :Precio_unitario)"
    values = {"Id_pedido": detalle_pedidos.Id_pedido,"Id_producto":detalle_pedidos.Id_producto, "Cantidad": detalle_pedidos.Cantidad, "Precio_unitario": detalle_pedidos.Precio_unitario}
    await database.execute(query=query, values=values)
    return {"message": "detalle_pedidos creado exitosamente", "data": detalle_pedidos}

# Listar detalle_pedidoss
@app.get("/detalle_pedidos/")
async def listar_detalle_pedidoss():
    query = "SELECT * FROM detalle_pedidos"
    return await database.fetch_all(query=query)

# Obtener detalle_pedidos por ID
@app.get("/detalle_pedidos/{detalle_pedidos_id}/")
async def obtener_detalle_pedidos(detalle_pedidos_id: int):
    query = "SELECT * FROM detalle_pedidos WHERE id = :id"
    values = {"Id_detalle_pedido": detalle_pedidos_id}
    detalle_pedidos = await database.fetch_one(query=query, values=values)
    if not detalle_pedidos:
        raise HTTPException(status_code=404, detail="detalle_pedidos no encontrado")
    return {"message": "Detalles del detalle_pedidos", "data": detalle_pedidos}

# Actualizar detalle_pedidos por ID
@app.put("/detalle_pedidos/{detalle_pedidos_id}/")
async def actualizar_detalle_pedidos(detalle_pedidos_id: int, detalle_pedidos: detalle_pedidos):
    query = "UPDATE detalle_pedidos SET Id_pedido = :Id_pedido, Id_producto = :Id_producto, Cantidad = :Cantidad, Precio_unitario = :Precio_unitario = :id"
    values = {"Id_detalle_pedido": detalle_pedidos_id, "Id_pedidos": detalle_pedidos.Id_pedido, "Id_producto": detalle_pedidos.Id_producto, "Cantidad": detalle_pedidos.Cantidad, "Precio_unitario":detalle_pedidos.Precio_unitario}
    await database.execute(query=query, values=values)
    return {"message": "detalle_pedidos actualizado exitosamente", "data": detalle_pedidos}

# Eliminar detalle_pedidos por ID
@app.delete("/detalle_pedidos/{detalle_pedidos_id}/")
async def eliminar_detalle_pedidos(detalle_pedidos_id: int):
    query = "DELETE FROM detalle_pedidos WHERE id = :id"
    values = {"id": detalle_pedidos_id}
    await database.execute(query=query, values=values)
    return {"message": "detalle_pedidos eliminado exitosamente", "detalle_pedidos_id": detalle_pedidos_id}