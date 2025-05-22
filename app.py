"""
API REST con Flask y MySQL
Autor: Nicole Stephanie Báez 
Descripción: Este script maneja usuarios en MySQL mediante una API REST.
Y hace uso de postMan
"""
from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

# Conectar con MySQL


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Coloca tu contraseña aquí
        database="mi_api_db"
    )


@app.route('/')
def inicio():
    return "API REST funcionando correctamente. Usa /usuarios para acceder."


@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    conn.close()
    return jsonify(usuarios)


@app.route('/usuarios', methods=['POST'])
def agregar_usuario():
    data = request.json
    nombre = data.get("nombre")
    edad = data.get("edad")

    if not nombre or not edad:
        return jsonify({"error": "Nombre y edad son obligatorios"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO usuarios (nombre, edad) VALUES (%s, %s)", (nombre, edad))
    conn.commit()
    conn.close()

    return jsonify({"mensaje": "Usuario agregado correctamente"}), 201


@app.route('/usuarios/<int:id>', methods=['PUT'])
def actualizar_usuario(id):
    data = request.json
    nombre = data.get("nombre")
    edad = data.get("edad")

    if not nombre or not edad:
        return jsonify({"error": "Nombre y edad son obligatorios"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE usuarios SET nombre=%s, edad=%s WHERE id=%s", (nombre, edad, id))
    conn.commit()
    conn.close()

    return jsonify({"mensaje": f"Usuario con ID {id} actualizado correctamente"})


@app.route('/usuarios/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id=%s", (id,))
    conn.commit()
    conn.close()

    return jsonify({"mensaje": f"Usuario con ID {id} eliminado correctamente"})


if __name__ == '__main__':
    app.run(debug=True)