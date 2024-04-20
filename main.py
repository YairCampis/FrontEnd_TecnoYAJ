from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr

import mysql.connector

app=FastAPI()

@app.get("/")
def endpoint():
    return {"Hola":" mundo mundial"}

class UserLogin(BaseModel):
    username: str
    password: str

@app.post("/login")
async def login(user: UserLogin):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="proyectoscul"
        )
        cursor = connection.cursor()

        # Ejecutar una consulta para verificar las credenciales del usuario
        query = "SELECT * FROM usuarios WHERE Nombre_usuario = %s AND Contraseña = %s"
        cursor.execute(query, (user.username, user.password))
        result = cursor.fetchone()

        if result:
            # Credenciales válidas, redirigir al usuario a la página de inicio
            return {"message": "Inicio de sesión exitoso"}
        else:
            # Credenciales inválidas, devolver un error
            raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    except mysql.connector.Error as err:
        print("Error al iniciar sesión:", err)
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    finally:
        cursor.close()
        connection.close()

# Definir modelo Pydantic para los datos del usuario
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

# Ruta para el registro de usuarios
@app.post("/register")
async def register_user(user: UserCreate):
    # Conectarse a la base de datos MySQL
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="proyectoscul"
    )

    cursor = connection.cursor()

    try:
        # Verificar si el usuario ya existe en la base de datos
        query = "SELECT Nombre_usuario, Email FROM usuarios WHERE Nombre_usuario = %s OR Email = %s"
        cursor.execute(query, (user.username, user.email))
        existing_user = cursor.fetchone()
        if existing_user:
            if existing_user[0] == user.username:
                raise HTTPException(status_code=400, detail="El nombre de usuario ya está en uso")
            if existing_user[1] == user.email:
                raise HTTPException(status_code=400, detail="La dirección de correo electrónico ya está en uso")

        # Insertar el nuevo usuario en la base de datos
        query = "INSERT INTO usuarios (Nombre_usuario, Email, Contraseña) VALUES (%s, %s, %s)"
        cursor.execute(query, (user.username, user.email, user.password))

        # Confirmar los cambios en la base de datos
        connection.commit()

        return {"message": "Usuario registrado exitosamente", "user_data": user.dict()}
    except mysql.connector.Error as err:
        print("Error al registrar el usuario:", err)
        raise HTTPException(status_code=500, detail="Error interno del servidor")
    finally:
        # Cerrar la conexión con la base de datos
        cursor.close()
        connection.close()
