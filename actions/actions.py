# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

import re
from typing import Any, Dict, List, Text
from rasa_sdk import Action
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.interfaces import Tracker
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
import ast
import pandas as pd


# Definisco il percorso del file CSV come variabile globale
PATH_TO_CSV = './dataset/cleaned/netflix_titles_cleaned.csv'

mappatura_generi_italiano = {
    'Classic Movies': ['classici', ' classic'],
    'Anime Series': ['anime', 'serie anime'],
    'TV Horror': ['horror', 'serie horror', 'horror tv'],
    'TV Mysteries': ['mistero', 'giallo', 'serie di mistero' ,'serie gialle', 'mistery'],
    'Children & Family Movies': ['famiglia', 'per bambini', ' per famiglie', 'neonati', 'infanzia', 'bambini', 'famiglie'],
    'Stand-Up Comedy': ['stand-up', 'comici stand-up', 'commedia stand-up','commedia nera', 'black-humor'],
    'Faith & Spirituality': ['spiritualità', 'fede e spiritualità', 'fede'],
    'TV Comedies': ['commedie tv', 'serie comiche','sitcom','comedy tv'],
    'TV Dramas': ['serie drammatica', 'drammi tv', 'serie drammatiche', 'serie drama', 'serie dramas'],
    'Science & Nature TV': ['scienza e natura', 'documentari scientifici', 'natura', 'scienza'],
    'Horror Movies': ['horror', ' spaventoso', 'dell\'orrore', 'orrore'],
    'Action & Adventure': ['azione e avventura', ' di azione', 'avventure', ' d\'avventura', 'avventura', 'azione', 'action'],
    'Sports Movies': ['sportivi', ' sportivi', 'sport'],
    'Crime TV Shows': ['tv crime', 'serie crime', 'gialli' ,'polizieschi'],
    'Documentaries': ['documentari', 'documentari tv'],
    'Stand-Up Comedy & Talk Shows': ['talk show', 'talk-show', 'talk shows'],
    'Korean TV Shows': ['coreani', 'serie coreane', 'k-drama'],
    'Music & Musicals': ['musical', 'musica e musical', 'musical tv', 'musica'],
    'Romantic TV Shows': ['romantico', 'serie romantiche', 'romanticismo tv show'],
    'Teen TV Shows': ['adolescenziali', 'serie per adolescenti', 'per ragazzini'],
    'Cult Movies': ['cult', 'culto'],
    'International Movies': ['internazionali', ' internazionali'],
    'Dramas': ['film drammatici', 'drammi', 'drama','film drammatico'],
    'British TV Shows': ['britannici', 'serie britanniche', 'british tv'],
    'Thrillers': ['thriller', 'gialli', ' thriller', 'suspense', 'suspense thriller'],
    'TV Action & Adventure': ['azione e avventura tv', 'serie di azione', 'avventura tv', 'serie d\'avventura', 'azione tv'],
    'Anime Features': ['anime', 'lungometraggi anime'],
    'LGBTQ Movies': ['lgbtq', ' LGBTQ', 'lgbtq+', 'lgbtqia+'],
    'Sci-Fi & Fantasy': ['film sci-fi', 'film fantasy', 'film fantascienza', 'film viaggi nel tempo'],
    'TV Thrillers': ['thriller tv', 'serie thriller'],
    'Classic & Cult TV': ['classici e cult', 'cult', 'classici della tv'],
    'International TV Shows': ['internazionali', 'internazionali'],
    "Kids' TV": ['per bambini', 'cartoni', 'programmi per bambini'],
    'Spanish-Language TV Shows': ['in spagnolo', 'spagnole', 'in spagnolo', 'spagnolo'],
    'Comedies': ['commedia', 'comiche', 'commedie', 'comici', 'comedy'],
    'Romantic Movies': ['film romantici', 'romanticismo', 'romantic'],
    'Reality TV': ['reality', 'reality show', 'programmi reality'],
    'Independent Movies': ['indipendenti', 'indie'],
    'Docuseries': ['docu-serie', 'documentaristiche', 'docuserie'],
    'TV Sci-Fi & Fantasy': ['serie di fantascienza', 'serie fantasy', 'serie sci-fi','viaggio nel tempo tv'],
}

mappatura_paesi = {
    "Italy": ["Italia", "italiano", "italiani"],
    "United States": ["Stati Uniti", "USA", "americano", "americani"],
    "France": ["Francia", "francese", "francesi"],
    "Germany": ["Germania", "tedesco", "tedeschi"],
    "United Kingdom": ["Regno Unito", "inglese", "inglesi", "britannico", "britannici"],
    "Canada": ["Canada", "canadese", "canadesi"],
    "Spain": ["Spagna", "spagnolo", "spagnoli"],
    "Australia": ["Australia", "australiano", "australiani"],
    "Japan": ["Giappone", "giapponese", "giapponesi"],
    "China": ["Cina", "cinese", "cinesi"],
    "Russia": ["Russia", "russo", "russi"],
    "India": ["India", "indiano", "indiani"],
    "Brazil": ["Brasile", "brasiliano", "brasiliani"],
    "Mexico": ["Messico", "messicano", "messicani"],
    "Argentina": ["Argentina", "argentino", "argentini"],
    "South Africa": ["Sudafrica", "sudafricano", "sudafricani"],
    "South Korea": ["Corea del Sud", "coreano", "coreani", "sudcoreano", "sudcoreani"],
    "Egypt": ["Egitto", "egiziano", "egiziani"],
    "Turkey": ["Turchia", "turco", "turchi"],
    "Netherlands": ["Paesi Bassi", "Olanda", "olandese", "olandes"],
    "Belgium": ["Belgio", "belga", "belgi"],
    "Sweden": ["Svezia", "svedese", "svedesi"],
    "Switzerland": ["Svizzera", "svizzero", "svizzeri"],
    "Norway": ["Norvegia", "norvegese", "norvegesi"],
    "Denmark": ["Danimarca", "danese", "danesi"],
    "Finland": ["Finlandia", "finlandese", "finlandesi"],
    "Poland": ["Polonia", "polacco", "polacchi"],
    "Austria": ["Austria", "austriaco", "austriaci"],
    "Ireland": ["Irlanda", "irlandese", "irlandesi"],
    "Portugal": ["Portogallo", "portoghese", "portoghesi"],
    "Greece": ["Grecia", "greco", "greci"],
    "Hungary": ["Ungheria", "ungherese", "ungheresi"],
    "Czech Republic": ["Repubblica Ceca", "ceco", "cechi"],
    "Slovakia": ["Slovacchia", "slovacco", "slovacchi"],
    "Slovenia": ["Slovenia", "sloveno", "sloveni"],
    "Croatia": ["Croazia", "croato", "croati"],
    "Serbia": ["Serbia", "serbo", "serbi"],
    "Afghanistan": ["Afghanistan", "afghano", "afghani"],
    "Albania": ["Albania", "albanese", "albanesi"],
    "Algeria": ["Algeria", "algerino", "algerini"],
    "Angola": ["Angola", "angolano", "angolani"],
    "Armenia": ["Armenia", "armeno", "armeni"],
    "Azerbaijan": ["Azerbaijan", "azero", "azeri"],
    "Bahamas": ["Bahamas"],
    "Bangladesh": ["Bangladesh", "bengalese", "bengalesi"],
    "Belarus": ["Bielorussia", "bielorusso", "bielorussi"],
    "Bermuda": ["Bermuda"],
    "Botswana": ["Botswana"],
    "Bulgaria": ["Bulgaria", "bulgaro", "bulgari"],
    "Burkina Faso": ["Burkina Faso"],
    "Cambodia": ["Cambogia", "cambogiano", "cambogiani"],
    "Cameroon": ["Camerun", "camerunese", "camerunesi"],
    "Cayman Islands": ["Isole Cayman"],
    "Chile": ["Cile", "cileno", "cileni"],
    "Colombia": ["Colombia", "colombiano", "colombiani"],
    "Cuba": ["Cuba", "cubano", "cubani"],
    "Cyprus": ["Cipro", "cipriota", "ciprioti"],
    "Dominican Republic": ["Repubblica Dominicana", "dominicano", "dominicani"],
    "East Germany": ["Germania Est", "tedesco orientale", "tedeschi orientali"],
    "Ecuador": ["Ecuador", "ecuadoriano", "ecuadoriani"],
    "Ethiopia": ["Etiopia", "etiopico", "etiopici"],
    "Georgia": ["Georgia", "georgiano", "georgiani"],
    "Ghana": ["Ghana", "ghanaiano", "ghanaians"],
    "Guatemala": ["Guatemala", "guatemalteco", "guatemaltechi"],
    "Hong Kong": ["Hong Kong", "hongkonghese", "hongkonghesi"],
    "Iceland": ["Islanda", "islandese", "islandesi"],
    "Indonesia": ["Indonesia", "indonesiano", "indonesiani"],
    "Iran": ["Iran", "iraniano", "iraniani"],
    "Iraq": ["Iraq", "iracheno", "iracheni"],
    "Jamaica": ["Giamaica", "giamaicano", "giamaicani"],
    "Jordan": ["Giordania", "giordano", "giordani"],
    "Kazakhstan": ["Kazakistan", "kazako", "kazaki"],
    "Kenya": ["Kenya", "keniota", "kenioti"],
    "Kuwait": ["Kuwait", "kuwaitiano", "kuwaitiani"],
    "Latvia": ["Lettonia", "lettone", "lettoni"],
    "Lebanon": ["Libano", "libanese", "libanesi"],
    "Liechtenstein": ["Liechtenstein"],
    "Lithuania": ["Lituania", "lituano", "lituani"],
    "Luxembourg": ["Lussemburgo", "lussemburghese", "lussemburghesi"],
    "Malawi": ["Malawi"],
    "Malaysia": ["Malesia", "malese", "malesi"],
    "Malta": ["Malta", "maltese", "maltesi"],
    "Mauritius": ["Mauritius", "mauriziano", "mauriziani"],
    "Mongolia": ["Mongolia", "mongolo", "mongoli"],
    "Morocco": ["Marocco", "marocchino", "marocchini"],
    "Mozambique": ["Mozambico", "mozambicano", "mozambicani"],
    "Namibia": ["Namibia", "namibiano", "namibiani"],
    "Nepal": ["Nepal", "nepalese", "nepalesi"],
    "New Zealand": ["Nuova Zelanda", "neozelandese", "neozelandesi"],
    "Nicaragua": ["Nicaragua", "nicaraguense", "nicaraguensi"],
    "Nigeria": ["Nigeria", "nigeriano", "nigeriani"],
    "Non disponibile": ["Non disponibile"],
    "Pakistan": ["Pakistan", "pachistano", "pachistani"],
    "Palestine": ["Palestina", "palestinese", "palestinesi"],
    "Panama": ["Panama", "panamense", "panamensi"],
    "Paraguay": ["Paraguay", "paraguaiano", "paraguayani"],
    "Peru": ["Perù", "peruviano", "peruviani"],
    "Philippines": ["Filippine", "filippino", "filippini"],
    "Puerto Rico": ["Porto Rico", "portoricano", "portoricani"],
    "Qatar": ["Qatar", "qatariota", "qatarioti"],
    "Samoa": ["Samoa", "samoano", "samoani"],
    "Saudi Arabia": ["Arabia Saudita", "saudita", "sauditi"],
    "Senegal": ["Senegal", "senegalese", "senegalesi"],
    "Singapore": ["Singapore", "singaporiano", "singaporiani"],
    "Somalia": ["Somalia", "somalo", "somali"],
    "Soviet Union": ["Unione Sovietica", "sovietico", "sovietici"],
    "Sri Lanka": ["Sri Lanka", "singalese", "singalesi"],
    "Sudan": ["Sudan", "sudanese", "sudanesi"],
    "Syria": ["Siria", "siriano", "siriani"],
    "Taiwan": ["Taiwan", "taiwanese", "taiwanesi"],
    "Uganda": ["Uganda", "ugandese", "ugandesi"],
    "Ukraine": ["Ucraina", "ucraino", "ucraini"],
    "United Arab Emirates": ["Emirati Arabi Uniti", "emiratino", "emiratini"],
    "Uruguay": ["Uruguay", "uruguaiano", "uruguayani"],
    "Vatican City": ["Città del Vaticano", "vaticano"],
    "Venezuela": ["Venezuela", "venezuelano", "venezuelani"],
    "Vietnam": ["Vietnam", "vietnamita", "vietnamiti"],
    "West Germany": ["Germania Ovest", "tedesco occidentale", "tedeschi occidentali"],
    "Zimbabwe": ["Zimbabwe", "zimbabwese", "zimbabwesi"]
}

mappatura_categorie = {
    'Adults Only - Not suitable for children under 17 years': ['solo maggiorenni', 'non adatto ai minori di 17 anni', 'maggiorenni'],
    'General - Suitable for all audiences': ['generale', 'adatto a tutti', 'per tutti'],
    'Kids - Suitable for all children': ['bambini', 'adatto ai bambini', 'per bambini', 'per i più piccoli' , 'per bambini piccoli'],
    'Mature - Suitable for adults only': ['maturi', 'adatto agli adulti', 'solo adulti', 'per adulti'],
    'Non Specificato': ['non specificato'],
    'Not Rated - No specific classification': ['non classificato', 'senza classificazione'],
    'Older Kids - Suitable for children over 7 years': ['ragazzi più grandi', 'adatto a bambini oltre i 7 anni'],
    'Older Kids - Suitable for children over 7 years with fantasy violence elements': ['ragazzi più grandi con elementi di violenza fantastica', 'bambini oltre i 7 anni con violenza fantastica'],
    'Parental Guidance - Parents urged to give parental guidance under 12 years': ['guida genitoriale', 'consigliato la guida dei genitori sotto i 12 anni'],
    'Parental Guidance Suggested - Suitable for children with parental guidance': ['guida genitoriale suggerita', 'adatto con guida dei genitori'],
    'Restricted - Suitable for adults (contains adult material)': ['ristretto', 'adatto agli adulti (contiene materiale per adulti)'],
    'Teens - Suitable for over 13 years': ['adolescenti', 'adatto a ragazzi oltre i 13 anni'],
    'Teens - Suitable for over 14 years': ['adolescenti oltre i 14 anni'],
    'Unrated - Uncensored or extended version not submitted for classification': ['non valutato', 'versione non censurata o estesa non sottoposta a classificazione']
}

def trova_corrispondenza(input_utente, mappa_corrispondenza):
    # Verifica se l'input corrisponde direttamente a una chiave
    if input_utente.title() in mappa_corrispondenza:
        return input_utente.title()

    # Verifica se l'input corrisponde a uno dei valori e ottiene la chiave corrispondente
    for chiave, valori in mappa_corrispondenza.items():
        if input_utente.lower() in [v.lower() for v in valori]:
            return chiave

    # Fuzzy matching come fallback
    tutte_le_chiavi = list(mappa_corrispondenza.keys())
    corrispondenza, punteggio = process.extractOne(input_utente, tutte_le_chiavi)
    if punteggio > 80:  # Soglia di accettazione per il fuzzy matching
        return corrispondenza

    return None  # Nessuna corrispondenza trovata

def cerca_con_fuzzy(entity_value, lookup_dict):
    for key, values in lookup_dict.items():
        if entity_value.lower() in [v.lower() for v in values]:
            return key
    keys = list(lookup_dict.keys())
    best_match, score = process.extractOne(entity_value, keys, scorer=fuzz.token_sort_ratio)
    if score > 80:
        return best_match
    return None

class ActionRicercaContenutiCSV(Action):
    def name(self) -> Text:
        return "action_ricerca_contenuti_csv"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        df = pd.read_csv(PATH_TO_CSV, converters={"genres_list": ast.literal_eval})
        entita_riconosciute = tracker.latest_message['entities']
        query = {}

        for entita in entita_riconosciute:
            if entita['entity'] in ['attore', 'regista']:
                entita_lista = df[entita['entity']].dropna().unique()
                matched_name = cerca_con_fuzzy(entita['value'], {e: [e] for e in entita_lista})
                if matched_name:
                    query[entita['entity']] = matched_name
            elif entita['entity'] == 'genere':
                matched_genre = trova_corrispondenza(entita['value'], mappatura_generi_italiano)
                if matched_genre:
                    query['genres_list'] = [matched_genre]
            elif entita['entity'] == 'paese':
                matched_country = trova_corrispondenza(entita['value'], mappatura_paesi)
                if matched_country:
                    query['country'] = matched_country
            elif entita['entity'] == 'categoria':
                matched_category = trova_corrispondenza(entita['value'], mappatura_categorie)
                if matched_category:
                    query['rating_category'] = matched_category
            elif entita['entity'] == 'tipo':
                tipo_valori = ['film', 'movie', 'titolo', 'pellicola', 'serie', 'tv show']
                matched_type = process.extractOne(entita['value'].lower(), tipo_valori, scorer=fuzz.token_set_ratio)
                if matched_type[1] > 80:
                    query['type'] = 'Movie' if matched_type[0] in ['film', 'movie', 'titolo', 'pellicola'] else 'TV Show'
            elif entita['entity'] == 'anno':
                query['release_year'] = int(entita['value'])
            elif entita['entity'] == 'durata':
                # Estrazione del numero e dell'unità dalla durata
                durata_match = re.search(r'(\d+)\s*(minuti|stagioni|stagione|min)', entita['value'], re.IGNORECASE)
                if durata_match:
                    numero, unita = durata_match.groups()
                    if 'min' in unita.lower():
                        query['duration_number'] = float(numero)
                        query['duration_unit'] = 'min'
                    else:
                        query['seasons'] = int(numero)

        # Applica i filtri basati sulla query costruita dalle entità
        for key, value in query.items():
            if key == 'attore' or key == 'regista':
                df = df[df[key].str.contains(value, case=False, na=False)]
            elif key == 'genres_list':
                df = df[df['genres_list'].apply(lambda genres: any(genre for genre in genres if genre in value))]
            elif key == 'country':
                df = df[df['country'].str.contains(value, case=False, na=False)]
            elif key == 'rating_category':
                df = df[df['rating_category'] == value]
            elif key == 'type':
                df = df[df['type'] == value]
            elif key == 'release_year':
                df = df[df['release_year'] == int(value)]
            elif key == 'duration_number':
                if query.get('duration_unit') == 'min':
                    df = df[(df['duration_number'] <= value) & (df['duration_unit'] == 'min')]
                else:  # Gestione delle stagioni per le serie TV
                    df = df[(df['seasons'] <= value) & (df['type'] == 'TV Show')]

        # Invio dei risultati
        if df.empty:
            dispatcher.utter_message(text="Non ho trovato risultati corrispondenti alla tua ricerca.")
        else:
            risultati = df.head(5)
            intro = "Ecco i risultati trovati"
            if 'type' in query:
                tipo_contenuto = "film" if query['type'] == 'Movie' else "serie TV"
                intro = f"Ecco i {tipo_contenuto} trovati"
            else:
                intro = "Ecco i contenuti trovati"
            
            filtri_applicati = []
            for k, v in query.items():
                if k == 'type':
                    continue
                elif k == 'genres_list':
                    filtri_applicati.append(f"genere: {', '.join([g.title() for g in v])}")
                elif k in ['attore', 'regista']:
                    filtri_applicati.append(f"{k}: {v.title()}")
                else:
                    filtri_applicati.append(f"{k}: {str(v).title()}")

            if filtri_applicati:
                intro += f" con i seguenti filtri: {', '.join(filtri_applicati)}."

            risposta = f"{intro}\n\n"
            for index, row in risultati.iterrows():
                titolo = row['title'].title()
                tipo = row['type']
                descrizione = row['description']
                if tipo == 'Movie':
                    durata = f"{row.get('duration_number', 'N/D')} min" if 'duration_number' in row else 'N/D'
                else:
                    durata = f"{row.get('seasons', 'N/D')} stagioni" if 'seasons' in row else 'N/D'
                risposta += f"- {titolo} ({'Film' if tipo == 'Movie' else 'Serie TV'}, Durata: {durata}):\n  Descrizione: {descrizione}\n\n"

            dispatcher.utter_message(text=risposta)

            return []


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

#  # Funziona bene
# class ActionGetMoviesByActor(Action):

#     def name(self) -> Text:
#         return "action_get_movies_by_actor"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         # Carica il dataset
#         df = pd.read_csv(PATH_TO_CSV)

#         # Normalizza i dati del cast rimuovendo spazi extra e convertendo tutto in lowercase
#         df['cast'] = df['cast'].apply(lambda x: ', '.join([actor.strip() for actor in x.split(',')]).lower() if isinstance(x, str) else x)

#         # Estraiamo il nome dell'attore dall'ultimo messaggio dell'utente
#         actor_query = tracker.latest_message.get('text').lower()

#         # Utilizziamo fuzzy matching per trovare la corrispondenza più vicina dell'attore nel cast
#         actors_list = df['cast'].str.split(', ').explode().unique()
#         actor_match = process.extractOne(actor_query, actors_list, score_cutoff=80)

#         if actor_match is None:
#             dispatcher.utter_message(text="Mi dispiace, non ho trovato film con l'attore che hai inserito.")
#             return []

#         # Estraiamo il nome dell'attore corrispondente
#         matched_actor = actor_match[0]

#         # Filtriamo il dataframe per i film in cui l'attore appare
#         filtered_df = df[df['cast'].apply(lambda x: matched_actor in x.split(', ') if isinstance(x, str) else False)]

#         if filtered_df.empty:
#             dispatcher.utter_message(text=f"Mi dispiace, non ho trovato film con l'attore {matched_actor}.")
#             return []

#         # Prepariamo e inviamo il messaggio con i risultati
#         movies_list = filtered_df[['title', 'genres_list']].values.tolist()
#         movies_text = f"{matched_actor} è apparso nei seguenti {len(movies_list)} film:\n" + \
#                       "\n".join([f"'{title}' - Genere: {genres}" for title, genres in movies_list])

#         dispatcher.utter_message(text=movies_text)

#         return []
