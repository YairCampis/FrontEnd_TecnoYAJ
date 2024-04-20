from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from databases import Database
import mysql.connector

app = FastAPI()

# Configuración de la base de datos
DATABASE_URL = "mysql+mysqlconnector://root:@localhost/proyectoscul"
database = Database(DATABASE_URL)

# Modelo de usuario
class Usuario(BaseModel):
    id: int
    usuario: str
    cc:int
    email: str
    contraseña: str
    telefono:int
    rol:str


# Crear usuario
@app.post("/usuarios/")
async def crear_usuario(usuario: Usuario):
    query = "INSERT INTO usuarios (usuario,cc,email,contraseña,telefono,rol) VALUES (:usuario, :cc, :email, :contraseña, :telefono, :rol)"
    values = {"usuario": usuario.usuario,"cc":usuario.cc, "email": usuario.email, "contraseña": usuario.contraseña,"telefono":usuario.telefono,"rol":usuario.rol}
    await database.execute(query=query, values=values)
    return {"message": "Usuario creado exitosamente", "data": usuario}

# Listar usuarios
@app.get("/usuarios/")
async def listar_usuarios():
    query = "SELECT * FROM usuarios"
    return await database.fetch_all(query=query)

# Obtener usuario por ID
@app.get("/usuarios/{usuario_id}/")
async def obtener_usuario(usuario_id: int):
    query = "SELECT * FROM usuarios WHERE id = :id"
    values = {"id": usuario_id}
    usuario = await database.fetch_one(query=query, values=values)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Detalles del usuario", "data": usuario}

# Actualizar usuario por ID
@app.put("/usuarios/{usuario_id}/")
async def actualizar_usuario(usuario_id: int, usuario: Usuario):
    query = "UPDATE usuarios SET usuario = :usuario, email = :email, contraseña = :contraseña WHERE id = :id"
    values = {"id": usuario_id, "usuario": usuario.usuario, "email": usuario.email, "contraseña": usuario.contraseña}
    await database.execute(query=query, values=values)
    return {"message": "Usuario actualizado exitosamente", "data": usuario}

# Eliminar usuario por ID
@app.delete("/usuarios/{usuario_id}/")
async def eliminar_usuario(usuario_id: int):
    query = "DELETE FROM usuarios WHERE id = :id"
    values = {"id": usuario_id}
    await database.execute(query=query, values=values)
    return {"message": "Usuario eliminado exitosamente", "usuario_id": usuario_id}
