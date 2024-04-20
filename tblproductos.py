from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from databases import Database
import mysql.connector

app = FastAPI()

# Configuración de la base de datos
DATABASE_URL = "mysql+mysqlconnector://root:@localhost/proyectoscul"
database = Database(DATABASE_URL)

# Modelo de Producto
class Producto(BaseModel):
    id_Producto: int
    Nombre_producto: str
    Referencia:str
    Precio: str
    Categoria: str
    Stock_Disponible:int


# Crear Producto
@app.post("/productos/")
async def crear_producto(usuarioproducto: Producto):
    query = "INSERT INTO productos (Nombre_producto,Referencia,Precio,Categoria,Stock_Disponible) VALUES (:Nombre_producto, :Referencia, :Precio, :Categoria, :Stock_Disponible)"
    values = {"Nombre_producto": Producto.Nombre_producto,"Referencia":Producto.Referencia, "Precio": Producto.Precio, "Categoria": Producto.Categoria,"Stock_Disponible":Producto.Stock_Disponible}
    await database.execute(query=query, values=values)
    return {"message": "Producto creado exitosamente", "data": Producto}

# Listar productos
@app.get("/productos/")
async def listar_productos():
    query = "SELECT * FROM productos"
    return await database.fetch_all(query=query)

# Obtener producto por ID
@app.get("/productos/{producto_id}/")
async def obtener_producto(producto_id: int):
    query = "SELECT * FROM productos WHERE id = :id"
    values = {"id_Producto": producto_id}
    Producto = await database.fetch_one(query=query, values=values)
    if not Producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"message": "Detalles del producto", "data": Producto}

# Actualizar producto por ID
@app.put("/productos/{producto_id}/")
async def actualizar_producto(producto_id: int, producto: Producto):
    query = "UPDATE productos SET Nombre_producto = :Nombre_producto, Referencia = :Referencia, Precio = :Precio, Categoria =:Categoria, Stock_Disponible=:Stock_Disponible WHERE id = :id"
    values = {"id_Producto": producto_id, "Nombre_producto": producto.Nombre_producto, "Referencia": producto.Referencia, "Precio": producto.Precio,"Categoria": producto.Categoria,"Stock_Disponible": producto.Stock_Disponible}
    await database.execute(query=query, values=values)
    return {"message": "producto actualizado exitosamente", "data": producto}

# Eliminar producto por ID
@app.delete("/productos/{producto_id}/")
async def eliminar_producto(producto_id: int):
    query = "DELETE FROM productos WHERE id = :id"
    values = {"id_Producto": producto_id}
    await database.execute(query=query, values=values)
    return {"message": "Producto eliminado exitosamente", "producto_id": producto_id}