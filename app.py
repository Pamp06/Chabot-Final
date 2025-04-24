from flask import Flask, render_template, request, jsonify
from chat import get_response, get_initial_message
from bs4 import BeautifulSoup
import sqlite3

app = Flask(__name__)

@app.get("/")
def index_get():
    return render_template("base.html")
    
@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    response_data = get_response(text) 
    
    if 'raw_html' in response_data:
        response_data['formatted_html'] = response_data['raw_html']
        
    return jsonify(response_data)

@app.get("/initial_message")
def initial_message():
    initial_data = get_initial_message()
    return jsonify(initial_data)
  
@app.post("/guardar_recomendacion")
def guardar_recomendacion():
    data = request.get_json()
    mensaje = data.get("mensaje")
    usuario = data.get("usuario", "")
    
    try:
        conn = sqlite3.connect('chatbotf.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Recomendaciones (Mensaje, Usuario) VALUES (?, ?)", (mensaje, usuario))
        conn.commit()
        conn.close()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="localhost", port=80, debug=False) #ruta ip local 0.0.0.0