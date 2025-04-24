if __name__=='__main__':
    import multiprocessing
    multiprocessing.freeze_support()
import sqlite3
import json
from nltk_utils import tokenize, stem, bag_of_words
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset,DataLoader
from model import NeuralNet

def entrenamiento():
    try:
        conn = sqlite3.connect('chatbotf.db')
        cursor = conn.cursor()

        cursor.execute("""
            SELECT i.Tag, p.Pattern, r.Response, b.Text, b.Value
            FROM Intents i
            INNER JOIN Patterns p ON i.Id = p.IntentId
            INNER JOIN Responses r ON i.Id = r.IntentId
            LEFT JOIN Buttons b ON i.Id = b.IntentId
        """)

        data = {
            "intents": []
        }

        intent_dict = {}

        for row in cursor:
            tag, pattern, response, button_text, button_value = row
            
            cleaned_response = response.strip()
            
            if tag not in intent_dict:
                intent_dict[tag] = {
                    "tag": tag,
                    "patterns": [],
                    "responses": [cleaned_response],
                    "buttons": []
                }
            else:
                if cleaned_response not in intent_dict[tag]["responses"]:
                    intent_dict[tag]["responses"].append(cleaned_response)
            
            if pattern not in intent_dict[tag]["patterns"]:
                intent_dict[tag]["patterns"].append(pattern)
            
            if button_text and button_value:
                button = {"text": button_text, "value": button_value}
                if button not in intent_dict[tag]["buttons"]:
                    intent_dict[tag]["buttons"].append(button)

        data["intents"] = list(intent_dict.values())

        with open('intents.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        cursor.close()
        conn.close()

        with open('intents.json', 'r', encoding='utf-8') as f:
            intents = json.load(f)

        all_words = []
        tags = []
        xy = []
        for intent in intents['intents']:
            tag = intent['tag']
            tags.append(tag)
            for pattern in intent['patterns']:
                w = tokenize(pattern)
                all_words.extend(w)
                xy.append((w, tag))

        ignore_words = ["?", "!", "¿", "¡", ",", ";", ":", "/", "="]

        all_words = [stem(w) for w in all_words if w not in ignore_words]
        all_words = sorted(set(all_words))
        tags = sorted(set(tags))

        x_train = []
        y_train = []

        for (pattern_sentence, tag) in xy:
            bag = bag_of_words(pattern_sentence, all_words)
            x_train.append(bag)

            label = tags.index(tag)
            y_train.append(label)

        x_train = np.array(x_train)
        y_train = np.array(y_train)

        class ChatDataset(Dataset):
            def __init__(self):
                self.n_samples = len(x_train)
                self.x_data = x_train
                self.y_data = y_train
            
            def __getitem__(self, index):
                return self.x_data[index], self.y_data[index]
            
            def __len__(self):
                return self.n_samples

        batch_size = 8
        hidden_size = 16
        output_size = len(tags)
        input_size = len(x_train[0])
        learning_rate = 0.01
        num_epochs = 2000

        dataset = ChatDataset()
        train_loader = DataLoader(dataset=dataset, batch_size=batch_size, shuffle=True)

        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model = NeuralNet(input_size, hidden_size, output_size).to(device)

        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

        for epoch in range(num_epochs):
            for (words, labels) in train_loader:
                words = words.to(device)
                labels = labels.to(device, dtype=torch.int64)

                outputs = model(words)
                loss = criterion(outputs, labels)
                
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

            if (epoch + 1) % 100 == 0:
                print(f'epoch {epoch + 1}/{num_epochs}, loss={loss.item():.4f}')

        print(f'final loss, loss={loss.item():.4f}')

        data = {
            "model_state": model.state_dict(),
            "input_size": input_size,
            "output_size": output_size,
            "hidden_size": hidden_size,
            "all_words": all_words,
            "tags": tags
        }

        FILE = "data.pth"
        torch.save(data, FILE)

        print(f'Entrenamiento completado, guardado en el archivo "{FILE}"')
        return True

    except IndexError as e:
        raise IndexError("No hay suficientes datos para entrenar el modelo. Asegúrate de que los campos estén llenos.") from e
    except Exception as e:
        raise Exception(f"Ocurrió un error durante el entrenamiento: {str(e)}") from e