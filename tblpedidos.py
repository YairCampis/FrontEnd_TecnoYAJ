from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from databases import Database
import mysql.connector

app = FastAPI()

# Configuración de la base de datos
DATABASE_URL = "mysql+mysqlconnector://root:@localhost/proyectoscul"
database = Database(DATABASE_URL)

# Modelo de pedidos
class Pedido(BaseModel):
    Id_pedido: int
    Id_usuario: int
    Fecha_pedido:int
    Estado: str


# Crear pedido
@app.post("/pedidos/")
async def crear_pedido(pedido: Pedido):
    query = "INSERT INTO pedidos (Id_pedido,Id_usuario,Fecha_pedido,Estado) VALUES (:Id_pedido, :Id_pedido, :Fecha_pedido, :Estado)"
    values = {"Id_pedido": pedido.Id_pedido,"Id_usuario":pedido.Id_usuario, "Fecha_pedido": pedido.Fecha_pedido, "Estado": pedido.Estado}
    await database.execute(query=query, values=values)
    return {"message": "pedido creado exitosamente", "data": pedido}

# Listar pedidos
@app.get("/pedidos/")
async def listar_pedidos():
    query = "SELECT * FROM pedidos"
    return await database.fetch_all(query=query)

# Obtener pedido por ID
@app.get("/pedidos/{pedido_id}/")
async def obtener_pedido(pedido_id: int):
    query = "SELECT * FROM pedidos WHERE id = :id"
    values = {"Id_pedido": pedido_id}
    pedido = await database.fetch_one(query=query, values=values)
    if not pedido:
        raise HTTPException(status_code=404, detail="pedido no encontrado")
    return {"message": "Detalles del pedido", "data": pedido}

# Actualizar pedido por ID
@app.put("/pedidos/{pedido_id}/")
async def actualizar_pedido(pedido_id: int, pedido: Pedido):
    query = "UPDATE pedidos SET pedido = :pedido, email = :email, contraseña = :contraseña WHERE id = :id"
    values = {"id": pedido_id, "pedido": pedido.pedido, "email": pedido.email, "contraseña": pedido.contraseña}
    await database.execute(query=query, values=values)
    return {"message": "pedido actualizado exitosamente", "data": pedido}

# Eliminar pedido por ID
@app.delete("/pedidos/{pedido_id}/")
async def eliminar_pedido(pedido_id: int):
    query = "DELETE FROM pedidos WHERE id = :id"
    values = {"id": pedido_id}
    await database.execute(query=query, values=values)
    return {"message": "pedido eliminado exitosamente", "pedido_id": pedido_id}