# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pandas as pd

# Definisco il percorso del file CSV come variabile globale
PATH_TO_CSV = './dataset/cleaned/netflix_titles_cleaned.csv'

mappatura_generi_italiano = {
    'Classic Movies': 'classici',
    'Anime Series': 'anime',
    'TV Horror': 'horror',
    'TV Mysteries': 'mistero',
    'Children & Family Movies': 'famiglia',
    'Stand-Up Comedy': 'stand-up',
    'Faith & Spirituality': 'spiritualità',
    'TV Comedies': 'commedia',
    'TV Dramas': 'drammatico',
    'Science & Nature TV': 'scienza e natura',
    'Horror Movies': 'horror',
    'Action & Adventure': 'azione e avventura',
    'Movies': 'film',
    'Sports Movies': 'sportivi',
    'Crime TV Shows': 'crime',
    'Documentaries': 'documentari',
    'Stand-Up Comedy & Talk Shows': 'commedia e talk show',
    'Korean TV Shows': 'coreani',
    'TV Shows': 'serie tv',
    'Music & Musicals': 'musical',
    'Romantic TV Shows': 'romantico',
    'Teen TV Shows': 'adolescenziali',
    'Cult Movies': 'cult',
    'International Movies': 'internazionali',
    'Dramas': 'drammatici',
    'British TV Shows': 'britannici',
    'Thrillers': 'thriller',
    'TV Action & Adventure': 'azione e avventura',
    'Anime Features': 'anime',
    'LGBTQ Movies': 'lgbtq',
    'Sci-Fi & Fantasy': 'fantascienza e fantasy',
    'TV Thrillers': 'thriller',
    'Classic & Cult TV': 'classici e cult',
    'International TV Shows': 'internazionali',
    "Kids' TV": 'per bambini',
    'Spanish-Language TV Shows': 'in spagnolo',
    'Comedies': 'commedia',
    'Romantic Movies': 'romantici',
    'Reality TV': 'reality',
    'Independent Movies': 'indipendenti',
    'Independent Movies': 'indie',
    'Docuseries': 'docu-serie',
    'TV Sci-Fi & Fantasy': 'fantascienza',
    'TV Sci-Fi & Fantasy': 'fantasy'
}




class ActionRicercaPerAttore(Action):

    def name(self) -> Text:
        return "action_ricerca_per_attore"

    async def run(self, dispatcher, tracker, domain):
        attore = tracker.get_slot('attore')
        tipo = tracker.get_slot('tipo')
        df = pd.read_csv(PATH_TO_CSV)
        
        if tipo == "film" or tipo == "movie" or tipo == "titoli":
            risultati = df[(df['cast'].str.contains(attore, case=False, na=False)) & (df['type'] == "Movie")]
        elif tipo == "serie TV" or tipo == "tv show" or tipo == "tv" or tipo == "serie":
            risultati = df[(df['cast'].str.contains(attore, case=False, na=False)) & (df['type'] == "TV Show")]
        else:
            # Fallback se il tipo non è specificato
            risultati = df[df['cast'].str.contains(attore, case=False, na=False)]

        if risultati.empty:
            dispatcher.utter_message(text=f"Mi dispiace, non ho trovato {tipo} con l'attore {attore}.")
        else:
            titoli = ",\n ".join(risultati['title'].tolist())
            dispatcher.utter_message(text=f"Ecco alcuni {tipo} con l'attore {attore}: {titoli}")

        return []


class ActionRicercaPerGenere(Action):
    
        def name(self) -> Text:
            return "action_ricerca_per_genere"
    
        async def run(self, dispatcher, tracker, domain):
            genere = tracker.get_slot('genere')
            tipo = tracker.get_slot('tipo')
            df = pd.read_csv(PATH_TO_CSV)
            genere = mappatura_generi_italiano.get(genere, genere)
    
            if tipo == "film" or tipo == "movie" or tipo == "titoli":
                risultati = df[(df['genres_list'].str.contains(genere, case=False, na=False)) & (df['type'] == "Movie")]
            elif tipo == "serie TV" or tipo == "tv show" or tipo == "tv" or tipo == "serie":
                risultati = df[(df['genres_list'].str.contains(genere, case=False, na=False)) & (df['type'] == "TV Show")]
            else:
                # Fallback se il tipo non è specificato
                risultati = df[df['genres_list'].str.contains(genere, case=False, na=False)]
    
            if risultati.empty:
                dispatcher.utter_message(text=f"Mi dispiace, non ho trovato {tipo} del genere {genere}.")
            else:
                titoli = ",\n ".join(risultati['title'].tolist())
                dispatcher.utter_message(text=f"Ecco alcuni {tipo} del genere {genere}: {titoli}")
    
            return []

class ActionRicercaPerPaese(Action):
    
        def name(self) -> Text:
            return "action_ricerca_per_paese"
    
        async def run(self, dispatcher, tracker, domain):
            paese = tracker.get_slot('paese')
            tipo = tracker.get_slot('tipo')
            df = pd.read_csv(PATH_TO_CSV)
    
            if tipo == "film" or tipo == "movie" or tipo == "titoli":
                risultati = df[(df['country'].str.contains(paese, case=False, na=False)) & (df['type'] == "Movie")]
            elif tipo == "serie TV" or tipo == "tv show" or tipo == "tv" or tipo == "serie":
                risultati = df[(df['country'].str.contains(paese, case=False, na=False)) & (df['type'] == "TV Show")]
            else:
                # Fallback se il tipo non è specificato
                risultati = df[df['country'].str.contains(paese, case=False, na=False)]
    
            if risultati.empty:
                dispatcher.utter_message(text=f"Mi dispiace, non ho trovato {tipo} del paese {paese}.")
            else:
                titoli = ",\n ".join(risultati['title'].tolist())
                dispatcher.utter_message(text=f"Ecco alcuni {tipo} del paese {paese}: {titoli}")
    
            return []
        
class ActionRicercaPerAnno(Action):
        
            def name(self) -> Text:
                return "action_ricerca_per_anno"
        
            async def run(self, dispatcher, tracker, domain):
                anno = tracker.get_slot('anno')
                tipo = tracker.get_slot('tipo')
                df = pd.read_csv(PATH_TO_CSV)
        
                if tipo == "film" or tipo == "movie" or tipo == "titoli":
                    risultati = df[(df['release_year'] == int(anno)) & (df['type'] == "Movie")]
                elif tipo == "serie TV" or tipo == "tv show" or tipo == "tv" or tipo == "serie":
                    risultati = df[(df['release_year'] == int(anno)) & (df['type'] == "TV Show")]
                else:
                    # Fallback se il tipo non è specificato
                    risultati = df[df['release_year'] == int(anno)]
        
                if risultati.empty:
                    dispatcher.utter_message(text=f"Mi dispiace, non ho trovato {tipo} dell'anno {anno}.")
                else:
                    titoli = ",\n ".join(risultati['title'].tolist())
                    dispatcher.utter_message(text=f"Ecco alcuni {tipo} dell'anno {anno}: {titoli}")
        
                return []
            
class ActionRicercaPerRegista(Action):
        
            def name(self) -> Text:
                return "action_ricerca_per_regista"
        
            async def run(self, dispatcher, tracker, domain):
                regista = tracker.get_slot('regista')
                tipo = tracker.get_slot('tipo')
                df = pd.read_csv(PATH_TO_CSV)
        
                if tipo == "film" or tipo == "movie" or tipo == "titoli":
                    risultati = df[(df['director'].str.contains(regista, case=False, na=False)) & (df['type'] == "Movie")]
                elif tipo == "serie TV" or tipo == "tv show" or tipo == "tv" or tipo == "serie":
                    risultati = df[(df['director'].str.contains(regista, case=False, na=False)) & (df['type'] == "TV Show")]
                else:
                    # Fallback se il tipo non è specificato
                    risultati = df[df['director'].str.contains(regista, case=False, na=False)]
        
                if risultati.empty:
                    dispatcher.utter_message(text=f"Mi dispiace, non ho trovato {tipo} diretti dal regista {regista}.")
                else:
                    titoli = ",\n ".join(risultati['title'].tolist())
                    dispatcher.utter_message(text=f"Ecco alcuni {tipo} diretti dal regista {regista}: {titoli}")
                
                return []

         
class ActionRicercaPerTitolo(Action):
    
    def name(self) -> Text:
        return "action_ricerca_per_titolo"

    async def run(self, dispatcher, tracker, domain):
        titolo_ricerca = tracker.get_slot('titolo')
        df = pd.read_csv(PATH_TO_CSV)
        risultati = df[df['title'].str.contains(titolo_ricerca, case=False, na=False)]

        if risultati.empty:
            dispatcher.utter_message(text=f"Mi dispiace, non ho trovato informazioni su {titolo_ricerca}.")
        else:
            # Formatta i risultati per mostrare informazioni specifiche in modo compatto
            info_formatted = []
            for _, row in risultati.iterrows():
                titolo = row['title']
                genere = row['genres_list']
                anno = row['release_year']
                descrizione = row['description'][:150] + "..." if len(row['description']) > 150 else row['description']
                
                # Costruisci il messaggio
                info = f"**Titolo**: {titolo}\n**Genere**: {genere}\n**Anno**: {anno}\n**Descrizione**: {descrizione}\n"
                info_formatted.append(info)
            
            # Unisci tutte le informazioni in un singolo messaggio
            message = "\n".join(info_formatted)
            dispatcher.utter_message(text=f"Ecco alcune informazioni che ho trovato su {titolo_ricerca}:\n{message}")

        return []


