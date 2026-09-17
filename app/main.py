import json
from typing import Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
 
app = FastAPI()
 
RUTA_JSON = "data/clientes.json"
 
# Modelo Pydantic para validar los datos recibidos en las peticiones
class ClienteModelo(BaseModel):
    nombre: str
    email: str
    telefono: str
 
 
# --- Funciones auxiliares para lectura y escritura en el archivo JSON ---
 
def cargar_clientes():
    try:
        with open(RUTA_JSON, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        return []
 
def guardar_clientes(clientes):
    with open(RUTA_JSON, "w", encoding="utf-8") as archivo:
        json.dump(clientes, archivo, indent=4, ensure_ascii=False)
 
 
# --- Rutas de la API ---
 
@app.get("/")
def inicio():
    return {"mensaje": "Generación de la API"}
 
# GET: Obtener todos los clientes
@app.get("/clientes")
def obtener_clientes():
    return cargar_clientes()
 
# GET: Obtener un cliente por ID
@app.get("/clientes/{id_cliente}")
def obtener_cliente(id_cliente: int):
    clientes = cargar_clientes()
    for cliente in clientes:
        if cliente["id"] == id_cliente:
            return cliente
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
 
# POST: Crear un nuevo cliente
@app.post("/clientes", status_code=status.HTTP_201_CREATED)
def crear_cliente(cliente: ClienteModelo):
    clientes = cargar_clientes()
    # Generar automáticamente un ID incremental
    nuevo_id = max([c["id"] for c in clientes], default=0) + 1
    nuevo_cliente = {
        "id": nuevo_id,
        "nombre": cliente.nombre,
        "email": cliente.email,
        "telefono": cliente.telefono
    }
    clientes.append(nuevo_cliente)
    guardar_clientes(clientes)
    return nuevo_cliente
 
# PUT: Actualizar un cliente existente
@app.put("/clientes/{id_cliente}")
def actualizar_cliente(id_cliente: int, cliente_actualizado: ClienteModelo):
    clientes = cargar_clientes()
    for i, cliente in enumerate(clientes):
        if cliente["id"] == id_cliente:
            datos_modificados = {
                "id": id_cliente,
                "nombre": cliente_actualizado.nombre,
                "email": cliente_actualizado.email,
                "telefono": cliente_actualizado.telefono
            }
            clientes[i] = datos_modificados
            guardar_clientes(clientes)
            return datos_modificados
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
 
# DELETE: Eliminar un cliente por ID
@app.delete("/clientes/{id_cliente}")
def eliminar_cliente(id_cliente: int):
    clientes = cargar_clientes()
    for i, cliente in enumerate(clientes):
        if cliente["id"] == id_cliente:
            cliente_eliminado = clientes.pop(i)
            guardar_clientes(clientes)
            return {
                "mensaje": f"Cliente con ID {id_cliente} eliminado correctamente",
                "cliente": cliente_eliminado
            }
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")