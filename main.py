from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
import mysql.connector

app = FastAPI()

# Conectar a la base de datos
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="proyectoscul"
)

cursor = db_connection.cursor()

# Ruta para servir la página HTML de login
@app.get("/", response_class=HTMLResponse)
async def mostrar_pagina_login():
    with open("login.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)

# Ruta para manejar el inicio de sesión
@app.post("/login")
async def procesar_login(email: str = Form(...), password: str = Form(...)):
    query = "SELECT * FROM usuarios WHERE email = %s AND password = %s"
    cursor.execute(query, (email, password))
    result = cursor.fetchone()
    if result:
        # Redireccionar al usuario a index.html después de una autenticación exitosa
        return RedirectResponse(url="/index.html")
    else:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
