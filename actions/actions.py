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
    'Classic Movies': 'Classici',
    'Anime Series': 'Serie Anime',
    'TV Horror': 'Serie Horror',
    'TV Mysteries': 'Gialli e Misteri',
    'Children & Family Movies': 'Film per Bambini e Famiglia',
    'Stand-Up Comedy': 'Comici Stand-Up',
    'Faith & Spirituality': 'Fede e Spiritualità',
    'TV Comedies': 'Commedie TV',
    'TV Dramas': 'Drammi TV',
    'Science & Nature TV': 'Scienza e Natura',
    'Horror Movies': 'Film Horror',
    'Action & Adventure': 'Azione e Avventura',
    'Movies': 'Film',
    'Sports Movies': 'Film Sportivi',
    'Crime TV Shows': 'Serie Crime',
    'Documentaries': 'Documentari',
    'Stand-Up Comedy & Talk Shows': 'Comici e Talk Show',
    'Korean TV Shows': 'Serie TV Coreane',
    'TV Shows': 'Serie TV',
    'Music & Musicals': 'Musica e Musical',
    'Romantic TV Shows': 'Serie TV Romantiche',
    'Teen TV Shows': 'Serie TV per Adolescenti',
    'Cult Movies': 'Film di Culto',
    'International Movies': 'Film Internazionali',
    'Dramas': 'Drammatici',
    'British TV Shows': 'Serie TV Britanniche',
    'Thrillers': 'Thriller',
    'TV Action & Adventure': 'Azione e Avventura TV',
    'Anime Features': 'Film Anime',
    'LGBTQ Movies': 'Film LGBTQ+',
    'Sci-Fi & Fantasy': 'Fantascienza e Fantasy',
    'TV Thrillers': 'Thriller TV',
    'Classic & Cult TV': 'TV Classica e di Culto',
    'International TV Shows': 'Serie TV Internazionali',
    "Kids' TV": 'TV per Bambini',
    'Spanish-Language TV Shows': 'Serie TV in Spagnolo',
    'Comedies': 'Commedie',
    'Romantic Movies': 'Film Romantici',
    'Reality TV': 'Reality',
    'Independent Movies': 'Film Indipendenti',
    'Docuseries': 'Serie Documentari',
    'TV Sci-Fi & Fantasy': 'Sci-Fi e Fantasy TV'
}


class ActionRicercaPerAttore(Action):

    def name(self) -> Text:
        return "action_ricerca_per_attore"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        
        attore = tracker.get_slot('attore')
        
        df = pd.read_csv(PATH_TO_CSV)  # Assicurati che il percorso sia corretto
        # Cerca attore nel campo 'Cast'
        risultati = df[df['Cast'].str.contains(attore, case=False, na=False)]
        
        if risultati.empty:
            dispatcher.utter_message(text=f"Mi dispiace, non ho trovato film con l'attore {attore}.")
        else:
            film = ", ".join(risultati['Titolo'].tolist())
            dispatcher.utter_message(text=f"Ecco alcuni film con l'attore {attore}: {film}")

        return []






class ActionRicercaPerGenere(Action):

    def name(self) -> Text:
        return "action_ricerca_per_genere"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        
        genere_italiano = tracker.get_slot('genere')
        # Converti il genere dall'italiano all'inglese usando la mappatura
        genere_inglese = mappatura_generi_italiano.get(genere_italiano, genere_italiano)  # Usa il valore italiano come fallback
        
        df = pd.read_csv(PATH_TO_CSV)  # Assicurati che il percorso sia corretto
        # Cerca genere in inglese nel campo 'Genere'
        risultati = df[df['Genere'].str.contains(genere_inglese, case=False, na=False)]
        
        if risultati.empty:
            dispatcher.utter_message(text=f"Mi dispiace, non ho trovato film di genere {genere_italiano}.")
        else:
            film = ", ".join(risultati['Titolo'].tolist())
            dispatcher.utter_message(text=f"Ecco alcuni film di genere {genere_italiano}: {film}")

        return []


