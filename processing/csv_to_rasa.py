import pandas as pd
import yaml

def csv_to_rasa_nlu(csv_filepath, yml_filepath):
    # Carica il dataset CSV
    df = pd.read_csv(csv_filepath)
    
    # Preparazione struttura dati per il file NLU di RASA
    rasa_nlu_data = {"nlu": []}
    intent_name = "faq"  # Nome generico dell'intento, personalizzalo come necessario

    # Aggiungi esempi all'intento
    examples = "\n".join(f"- {text}" for text in df["Text"])
    rasa_nlu_data["nlu"].append({
        "intent": intent_name,
        "examples": examples
    })
    
    # Scrive il file YML
    with open(yml_filepath, 'w', encoding='utf8') as file:
        yaml.dump(rasa_nlu_data, file, allow_unicode=True, sort_keys=False)

# Percorsi dei file
csv_filepath = './dataset/rsics_dataset/1_1_align.csv'  # Aggiorna con il percorso del tuo file CSV
yml_filepath = 'processing/nlu.yml'  # Aggiorna con il percorso desiderato per il file YML

# Esegui la conversione
csv_to_rasa_nlu(csv_filepath, yml_filepath)
