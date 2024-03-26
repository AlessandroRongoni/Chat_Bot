# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Dict, List, Text
from rasa_sdk import Action
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.interfaces import Tracker
from fuzzywuzzy import process
import ast
import pandas as pd


# Definisco il percorso del file CSV come variabile globale
PATH_TO_CSV = './dataset/cleaned/netflix_titles_cleaned.csv'

mappatura_generi_italiano = {
    'Classic Movies': ['classici', 'film classici'],
    'Anime Series': ['anime', 'serie anime'],
    'TV Horror': ['horror', 'serie horror', 'horror tv'],
    'TV Mysteries': ['mistero', 'giallo', 'serie di mistero'],
    'Children & Family Movies': ['famiglia', 'film per bambini', 'film per famiglie'],
    'Stand-Up Comedy': ['stand-up', 'comici stand-up', 'commedia stand-up','commedia nera', 'black-humor'],
    'Faith & Spirituality': ['spiritualità', 'fede e spiritualità', 'fede'],
    'TV Comedies': ['commedia', 'commedie tv', 'serie comiche'],
    'TV Dramas': ['drammatico', 'drammi tv', 'serie drammatiche'],
    'Science & Nature TV': ['scienza e natura', 'documentari scientifici', 'natura', 'scienza'],
    'Horror Movies': ['horror', 'film horror'],
    'Action & Adventure': ['azione e avventura', 'film di azione', 'avventure', 'film d\'avventura', 'avventura', 'azione', 'action'],
    'Movies': ['film', 'pellicole'],
    'Sports Movies': ['sportivi', 'film sportivi', 'sport'],
    'Crime TV Shows': ['crime', 'serie crime', 'gialli'],
    'Documentaries': ['documentari', 'documentari tv'],
    'Stand-Up Comedy & Talk Shows': ['commedia e talk show', 'stand-up e talk show', 'comici e talk show','talk show'],
    'Korean TV Shows': ['coreani', 'serie coreane', 'k-drama'],
    'TV Shows': ['serie tv', 'programmi tv', 'telefilm', 'serie televisive'],
    'Music & Musicals': ['musical', 'musica e musical', 'musical tv', 'musica'],
    'Romantic TV Shows': ['romantico', 'serie romantiche', 'romanticismo'],
    'Teen TV Shows': ['adolescenziali', 'serie per adolescenti'],
    'Cult Movies': ['cult', 'film cult'],
    'International Movies': ['internazionali', 'film internazionali'],
    'Dramas': ['drammatici', 'drammi', 'drama','film drammatico'],
    'British TV Shows': ['britannici', 'serie britanniche', 'british tv'],
    'Thrillers': ['thriller', 'gialli', 'film thriller', 'suspense', 'suspense thriller'],
    'TV Action & Adventure': ['azione e avventura tv', 'serie di azione', 'avventura tv', 'serie d\'avventura', 'azione tv'],
    'Anime Features': ['anime', 'lungometraggi anime'],
    'LGBTQ Movies': ['lgbtq', 'film lgbtq'],
    'Sci-Fi & Fantasy': ['film fantascienza e fantasy', 'film fantasy', 'film sci-fi', 'film fantascienza'],
    'TV Thrillers': ['thriller tv', 'serie thriller'],
    'Classic & Cult TV': ['classici e cult tv', 'serie cult', 'classici della tv'],
    'International TV Shows': ['internazionali', 'serie internazionali'],
    "Kids' TV": ['per bambini', 'cartoni', 'programmi per bambini'],
    'Spanish-Language TV Shows': ['in spagnolo', 'serie spagnole', 'serie in spagnolo', 'spagnolo'],
    'Comedies': ['commedia', 'comiche', 'commedie', 'commedie tv'],
    'Romantic Movies': ['romantici', 'film romantici'],
    'Reality TV': ['reality', 'reality show', 'programmi reality'],
    'Independent Movies': ['indipendenti', 'indie', 'film indie'],
    'Docuseries': ['docu-serie', 'serie documentaristiche', 'docuserie'],
    'TV Sci-Fi & Fantasy': ['fantascienza', 'fantasy', 'serie sci-fi', 'serie fantasy'],
}

# Funziona
class GetGeneriFromData(Action):

    def name(self) -> Text:
        return "action_get_generi_from_data"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Carica il dataset
        df = pd.read_csv(PATH_TO_CSV)

        # Estraiamo i generi, convertiamo da stringa a lista Python, e poi concateniamo tutto in un'unica lista
        all_genres = []
        for genres_string in df['genres_list']:
            genres_list = ast.literal_eval(genres_string)  # Converte la stringa in lista
            all_genres.extend(genres_list)  # Aggiunge gli elementi della lista alla lista all_genres

        # Otteniamo generi unici e li ordiniamo
        unique_genres = sorted(set(all_genres))

        # Creiamo la stringa per l'output, mettendo ogni genere su una nuova linea
        genres_message = "- " + "\n- ".join(unique_genres)

        # Creo il messaggio da inviare all'utente
        messaggio = "Ecco alcuni generi che potresti cercare:\n\n" + genres_message

        # Invio il messaggio
        dispatcher.utter_message(text=messaggio)

        return []
        
# Funziona
class ActionResetSlots(Action):

    def name(self) -> Text:
        return "action_reset_slots"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Ottieni l'elenco di tutti gli slot definiti nel dominio
        slots = tracker.slots.keys()

        # Crea un evento SlotSet per ogni slot impostandolo su None
        slot_values = [SlotSet(slot, None) for slot in slots]

        return slot_values

# Funziona    
class GetPaesiFromData(Action):

    def name(self) -> Text:
        return "action_get_paesi_from_data"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Carica il dataset
        df = pd.read_csv(PATH_TO_CSV)

        # Assumendo che i paesi siano separati da virgole in una singola colonna 'country'
        # Splitting di ogni riga sulla virgola e poi unire tutto in un'unica lista
        all_countries = []
        for country_string in df['country'].dropna():  # Usiamo dropna per escludere valori NaN
            countries_list = [country.strip() for country in country_string.split(',')]
            all_countries.extend(countries_list)

        # Otteniamo paesi unici e li ordiniamo
        unique_countries = sorted(set(all_countries))

        # Creiamo la stringa per l'output, mettendo ogni paese su una nuova linea
        countries_message = "- " + "\n- ".join(unique_countries)

        # Creo il messaggio da inviare all'utente
        messaggio = "Ecco alcuni paesi dai quali abbiamo contenuti:\n\n" + countries_message

        # Invio il messaggio
        dispatcher.utter_message(text=messaggio)

        return []

# Funziona
class ActionGetMoviesByActor(Action):

    def name(self) -> Text:
        return "action_get_movies_by_actor"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Carica il dataset
        df = pd.read_csv(PATH_TO_CSV)

        # Normalizza i dati del cast rimuovendo spazi extra e convertendo tutto in lowercase
        df['cast'] = df['cast'].apply(lambda x: ', '.join([actor.strip() for actor in x.split(',')]).lower() if isinstance(x, str) else x)

        # Estraiamo il nome dell'attore dall'ultimo messaggio dell'utente
        actor_query = tracker.latest_message.get('text').lower()

        # Utilizziamo fuzzy matching per trovare la corrispondenza più vicina dell'attore nel cast
        actors_list = df['cast'].str.split(', ').explode().unique()
        actor_match = process.extractOne(actor_query, actors_list, score_cutoff=70)

        if actor_match is None:
            dispatcher.utter_message(text="Mi dispiace, non ho trovato film con l'attore che hai inserito.")
            return []

        # Estraiamo il nome dell'attore corrispondente
        matched_actor = actor_match[0]

        # Filtriamo il dataframe per i film in cui l'attore appare
        filtered_df = df[df['cast'].apply(lambda x: matched_actor in x.split(', ') if isinstance(x, str) else False)]

        if filtered_df.empty:
            dispatcher.utter_message(text=f"Mi dispiace, non ho trovato film con l'attore {matched_actor}.")
            return []

        # Prepariamo e inviamo il messaggio con i risultati
        movies_list = filtered_df[['title', 'genres_list']].values.tolist()
        movies_text = f"{matched_actor} è apparso nei seguenti {len(movies_list)} film:\n" + \
                      "\n".join([f"'{title}' - Genere: {genres}" for title, genres in movies_list])

        dispatcher.utter_message(text=movies_text)

        return []

# Da testare
class ActionGetMoviesByDirector(Action):

    def name(self) -> Text:
        return "action_get_movies_by_director"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Carica il dataset
        df = pd.read_csv(PATH_TO_CSV)

        # Normalizza i dati del regista rimuovendo spazi extra e convertendo tutto in lowercase
        df['director'] = df['director'].apply(lambda x: ', '.join([director.strip() for director in x.split(',')]).lower() if isinstance(x, str) else x)

        # Estraiamo il nome del regista dall'ultimo messaggio dell'utente
        director_query = tracker.latest_message.get('text').lower()

        # Utilizziamo fuzzy matching per trovare la corrispondenza più vicina del regista
        directors_list = df['director'].str.split(', ').explode().unique()
        director_match = process.extractOne(director_query, directors_list, score_cutoff=70)

        if director_match is None:
            dispatcher.utter_message(text="Mi dispiace, non ho trovato film con il regista che hai inserito.")
            return []

        # Estraiamo il nome del regista corrispondente
        matched_director = director_match[0]

        # Filtriamo il dataframe per i film diretti dal regista trovato
        filtered_df = df[df['director'].apply(lambda x: matched_director in x.split(', ') if isinstance(x, str) else False)]

        if filtered_df.empty:
            dispatcher.utter_message(text=f"Mi dispiace, non ho trovato film con il regista {matched_director}.")
            return []

        # Prepariamo e inviamo il messaggio con i risultati
        movies_list = filtered_df[['title', 'genres_list']].values.tolist()
        movies_text = f"{matched_director} ha diretto i seguenti {len(movies_list)} film:\n" + \
                      "\n".join([f"'{title}' - Genere: {genres}" for title, genres in movies_list])

        dispatcher.utter_message(text=movies_text)

        return []
