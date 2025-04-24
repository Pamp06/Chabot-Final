import random
import json
import torch
from nltk_utils import tokenize, stem, bag_of_words
from model import NeuralNet
from bs4 import BeautifulSoup

contexto_actual = None

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r', encoding='utf-8') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE, weights_only=True)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Paulina"

# Funcion para el mensaje inicial del bot
def get_initial_message():
    welcome_message = f"¡Hola! Soy {bot_name}, tu asistente virtual. ¿En qué puedo ayudarte hoy?"
    
    return {
        "answer": welcome_message,
        "buttons": [{
            "text": "Empezar",
            "value": "Empezar"
        }],
        "raw_html": welcome_message
    }

def get_response(msg):
    global contexto_actual
    
    sentence = tokenize(msg)
    print(f"\n[DEBUG] Entrada: '{msg}'")
    print(f"[DEBUG] Tokenizado: {sentence}")
    
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)
    
    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    
    print(f"[DEBUG] Predicción: '{tag}' (Confianza: {prob.item():.2%})")
    
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                if tag == "carreras":
                    contexto_actual = "carreras"
                response = random.choice(intent['responses'])
                buttons = intent.get('buttons', [])
                
                formatted_response = response.replace('<br>', '\n').replace('&nbsp;', ' ')
                
                # Procesar otros formatos
                soup = BeautifulSoup(formatted_response, 'html.parser')
                formatted_response = ""
                for element in soup.children:
                    if element.name == 'b':
                        formatted_response += f"*{element.get_text()}*"
                    elif element.name == 'i':
                        formatted_response += f"_{element.get_text()}_"
                    elif element.name == 'u':
                        formatted_response += f"_{element.get_text()}_"
                    else:
                        formatted_response += str(element)
                
                return {
                    "answer": formatted_response,
                    "buttons": buttons,
                    "raw_html": response
                }
    else:
        return {
            "answer": "No entendí. ¿Podrías reformular tu pregunta?",
            "buttons": [
              {
                    "text": "Volver",
                    "value": "Empezar"
                }
            ]
        }

if __name__ == "__main__":
    print("Chatbot listo (escribe 'salir' para terminar)")
    
    # Mostrar mensaje inicial
    initial_message = get_initial_message()
    print(f"{bot_name}: {initial_message['answer']}")
    print("Opciones rápidas:", [btn['text'] for btn in initial_message['buttons']])
    
    while True:
        user_input = input("Tú: ")
        if user_input.lower() == "salir":
            break
            
        response_data = get_response(user_input)
        print(f"{bot_name}: {response_data['answer']}")
        if response_data['buttons']:
            print("Opciones rápidas:", [btn['text'] for btn in response_data['buttons']])