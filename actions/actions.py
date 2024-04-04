# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from datetime import datetime, timedelta
import re
from typing import Any, Dict, List, Text
from rasa_sdk import Action
from rasa_sdk.events import SlotSet, EventType, AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.interfaces import Tracker
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
from rasa_sdk.forms import FormValidationAction
from rasa_sdk.types import DomainDict
import logging
import ast
import pandas as pd

##### COSE DA FARE #####
# 6. Azione per consigliare in base alle preferenze  (FORM)
# 8. Migliorare ricerca per categoria
# 9. All'inizio il chatbot da una sua descrizione

# Definisco il percorso del file CSV come variabile globale
PATH_TO_CSV = './dataset/cleaned/netflix_titles_cleaned.csv'

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
    'Adults Only - Not suitable for children under 17 years': ['solo maggiorenni', 'non adatto ai minori di 17 anni', 'maggiorenni', 'Adults Only'],
    'General - Suitable for all audiences': ['generale', 'adatto a tutti', 'per tutti', 'anziani', 'per tutti i pubblici', 'tutti', 'general' ],
    'Kids - Suitable for all children': ['bambini', 'adatto ai bambini', 'per bambini', 'i più piccoli' , 'per bambini piccoli', 'Kids'],
    'Mature - Suitable for adults only': ['maturi', 'adatto agli adulti', 'solo adulti', 'per adulti','Mature'],
    'Non Specificato': ['non specificato'],
    'Not Rated - No specific classification': ['non classificato', 'senza classificazione', 'Not Rated', 'Non valutato'],
    'Older Kids - Suitable for children over 7 years': ['ragazzi più grandi', 'adatto a bambini oltre i 7 anni','Older Kids'],
    'Older Kids - Suitable for children over 7 years with fantasy violence elements': ['ragazzi più grandi con elementi di violenza fantastica', 'bambini oltre i 7 anni con violenza fantastica', 'Older Kids', 'fantasy violence'],
    'Parental Guidance - Parents urged to give parental guidance under 12 years': ['guida genitoriale', 'consigliato la guida dei genitori sotto i 12 anni','Parental Guidance', 'adatto con guida dei genitori'],
    'Parental Guidance Suggested - Suitable for children with parental guidance': ['guida genitoriale suggerita', 'adatto con guida dei genitori', 'Parental Guidance Suggested'],
    'Restricted - Suitable for adults (contains adult material)': ['ristretto', 'adatto agli adulti (contiene materiale per adulti)', 'Restricted'],
    'Teens - Suitable for over 13 years': ['adolescenti', 'adatto a ragazzi oltre i 13 anni', '13 Teens', 'teens'],
    'Teens - Suitable for over 14 years': ['adolescenti oltre i 14 anni', 'adatto a ragazzi oltre i 14 anni', '14 Teens', 'teens'],
    'Unrated - Uncensored or extended version not submitted for classification': ['non valutato', 'versione non censurata o estesa non sottoposta a classificazione', 'Unrated'],
}

mappatura_generi_film = {
    'Classic Movies': ['classici', 'classico', 'classic', 'epoca', 'vintage', 'anni 50', 'anni 60', 'anni 70', 'anni 80', 'anni 90'],
    'Horror Movies': ['horror', 'spaventoso', 'dell\'orrore', 'di paura', 'pauroso', 'terrificante','paura', 'spaventosi'],
    'Action & Adventure': ['azione e avventura', 'd\'azione', 'di avventura', 'action', 'avventuroso', 'avventura', 'azione', 'missioni', 'avventurieri'],
    'Sports Movies': ['sportivi', 'sport', 'sportivo', 'atleti', 'atletica', 'atletico'],
    'Documentaries': ['documentari', 'documentario', 'docufilm', 'docu', 'documentaristici', 'documentaristica', 'educativi', 'educazionali'],
    'Music & Musicals': ['musical', 'musica', 'cinema musicale', 'balli', 'danza', 'musicali', 'concerti'],
    'Cult Movies': ['cult', 'di culto'],
    'International Movies': ['internazionali', 'cinema mondiale', 'cinema estero', 'estere', 'stranieri', 'straniero'],
    'Dramas': ['drammatici', 'drammi', 'drama', 'opere drammatiche', 'drammatiche', 'drammatico', 'piangere','tristi', 'triste','emozionanti', 'emozionante', 'emozioni', 'emozionare'],
    'Thrillers': ['thriller', 'gialli', 'suspense', 'tensione', 'ansia', 'ansioso', 'suspensivi', 'suspenseful'],
    'Anime Features': ['anime', 'animazione giapponese', 'cartoni giapponesi', 'anime giapponesi', 'cartoni animati','animazione', 'cartoni', 'd\'animazione'],
    'LGBTQ Movies': ['lgbtq', 'tematiche lgbtq', 'lgbtq+', 'lgbtq friendly', 'lgbtq amichevole', 'lgbtq amichevoli'],
    'Sci-Fi & Fantasy': ['sci-fi', 'fantasy', 'fantascienza', 'viaggi spazio-temporali', 'mondi fantastici', 'fantasia', 'fantascientifici', 'fantascienza e fantasy'],
    'Comedies': ['commedia', 'comiche', 'commedie', 'comici', 'comico', 'comiche', 'divertenti', 'divertente', 'ridere', 'umorismo', 'umoristici', 'umoristico', 'comedy'],
    'Romantic Movies': ['romantici', 'romanticismo', 'cinema romantico', 'amore', 'storie d\'amore', 'romantico', 'romantica', 'romantiche'],
    'Independent Movies': ['indipendenti', 'indie', 'cinema indipendente', 'indipendente'],
    'Faith & Spirituality': ['spiritualità', 'fede e spiritualità', 'religione', 'religiosi', 'religioso', 'fede', 'Dio', 'Gesù', 'divinità','divino'],
    'Children & Family Movies': ['famiglia', 'per bambini', 'per famiglie', 'neonati', 'infanzia', 'bambini', 'famiglie', 'piccoli'],
}

mappatura_generi_serie_tv = {
    'Anime Series': ['anime', 'animazione giapponese', 'cartoni giapponesi', 'anime giapponesi', 'cartoni animati','animazione', 'cartoni', 'd\'animazione'],
    'TV Horror': ['horror', 'spaventoso', 'dell\'orrore', 'di paura', 'pauroso', 'terrificante','paura', 'spaventosi'],
    'TV Mysteries': ['mistero', 'giallo', 'di mistero', 'gialle', 'misteri', 'misteriosi', 'misterioso','suspanse', 'tensione'],
    'TV Comedies': ['commedia', 'comiche', 'commedie', 'comici', 'comico', 'comiche', 'divertenti', 'divertente', 'ridere', 'umorismo', 'umoristici', 'umoristico', 'comedy'],
    'Faith & Spirituality': ['spiritualità', 'fede e spiritualità', 'religione', 'religiosi', 'religioso', 'fede', 'Dio', 'Gesù', 'divinità','divino'],
    'TV Dramas': ['drammatici', 'drammi', 'drama', 'opere drammatiche', 'drammatiche', 'drammatico', 'piangere','tristi', 'triste','emozionanti', 'emozionante', 'emozioni', 'emozionare'],
    'Science & Nature TV': ['scienza e natura', 'documentari scientifici', 'natura','scienza', 'naturale'],
    'Crime TV Shows': ['crime', 'gialli', 'polizieschi', 'investigativi', 'investigazioni', 'investigativo', 'poliziesco'],
    'Stand-Up Comedy & Talk Shows': ['talk show', 'stand-up', 'standup'],
    'Korean TV Shows': ['coreani', 'k-drama', 'drammi coreani', 'corea'],
    'Romantic TV Shows': ['romantici', 'romanticismo', 'cinema romantico', 'amore', 'storie d\'amore', 'romantico', 'romantica', 'romantiche'],
    'Teen TV Shows': ['adolescenziali', 'per adolescenti', 'teen', 'giovani', 'teens', 'ragazzi', 'ragazze', 'amici', 'amicizia'],
    'British TV Shows': ['britannici', 'UK show', 'UK', 'inglesi', 'britannico'],
    'TV Action & Adventure': ['azione e avventura', 'd\'azione', 'di avventura', 'action', 'avventuroso', 'avventura', 'azione', 'missioni', 'avventurieri'],
    'TV Thrillers': ['thriller', 'suspense', 'tensione'],
    'Classic & Cult TV': ['cult', 'classici', 'culto'],
    'International TV Shows': ['internazionali', 'mondiali', 'estere'],
    "Kids' TV": ['per bambini', 'cartoni', 'infanzia', 'infantili'],
    'Spanish-Language TV Shows': ['in spagnolo', 'spagnole', 'lingua spagnola', 'drammi spagnoli'],
    'Reality TV': ['reality', 'vita reale', 'competizioni'],
    'Docuseries': ['docu serie', 'documentaristiche', 'inchieste'],
    'TV Sci-Fi & Fantasy': ['fantascienza', 'fantasy', 'mondi fantastici', 'avventure spaziali'],
    'Music & Musicals': ['musical', 'musica', 'cinema musicale', 'balli', 'danza', 'musicali', 'concerti'],
    
}

def merge_movie_titles(text: Text, entities: List[Dict]) -> Text:
    # Filtra solo le entità di tipo 'titolo'
    title_entities = [e for e in entities if e['entity'] == 'titolo']
    # Ordina le entità per la loro posizione di inizio
    title_entities.sort(key=lambda x: x['start'])
    # Unisci i valori delle entità per formare il titolo completo
    merged_title = ' '.join(e['value'] for e in title_entities)
    # Verifica che il titolo unificato sia presente nel testo originale
    # e corrisponda a un pattern che esclude comandi o altre parti non rilevanti
    patterns =[
        r"([A-Za-z0-9]+(?:['\-\.]?[A-Za-z0-9]+)*(?:\s+[A-Za-z0-9]+(?:['\-\.]?[A-Za-z0-9]+)*)*)",
        r"([A-Za-z0-9]+(?:['\-:\.\,]?[A-Za-z0-9]+)*(?:\s+[IVXLCDM]+)?(?:\s+[A-Za-z0-9]+(?:['\-:\.\,]?[A-Za-z0-9]+)*)*)",
        r"([A-Za-z0-9]+(?:['\-:\.\,]?[A-Za-z0-9]+)*\s*(?:\(\d{4}\))?(?:\s+[A-Za-z0-9]+(?:['\-:\.\,]?[A-Za-z0-9]+)*)*)",
        r"([A-Za-z0-9]+(?:['\-:\.\,]?[A-Za-z0-9]+)*\s*(?:Part\s+[IVXLCDM]+)?(?:[:]\s+[A-Za-z0-9]+(?:['\-:\.\,]?[A-Za-z0-9]+)*)*)",
        r"([A-Za-z0-9]+(?:['\-:\.\,]?[A-Za-z0-9]+)*\s*(?:\(\d{4}\))?(\s*[:]\s*[A-Za-z0-9]+(?:['\-:\.\,]?[A-Za-z0-9]+)*)*(?:\s+[IVXLCDM]+)?(?:\s+[A-Za-z0-9]+(?:['\-:\.\,]?[A-Za-z0-9]+)*)*)"
    ]

    for pattern in patterns:
        match = re.search(pattern, text)  # Cerca nel testo completo
        if match and merged_title.lower() in match.group(0).lower():
            return match.group(0)
    
    return ''

def isolate_title_from_request(text: Text) -> Text:
    # Rimuove parti comuni delle richieste che non fanno parte del titolo
    intro_phrases = ['info su', 'informazioni su', 'dettagli su']
    pattern = rf"\b(?:{'|'.join(intro_phrases)})\b\s*(.*)"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1)  # Restituisce il titolo isolato
    return text  # Se non trova il pattern, restituisce il testo originale

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
    if punteggio > 90:  # Soglia di accettazione per il fuzzy matching
        return corrispondenza

    return None  # Nessuna corrispondenza trovata

def infer_role_from_context(text: Text, entity_start: int) -> Text:
    # Definiamo una "finestra" di testo che precede l'entità
    window_start = max(0, entity_start - 70)  # Aumentiamo la finestra a 50 caratteri
    preceding_text = text[window_start:entity_start].lower()
    # Definiamo una lista di possibili parole chiave per ogni ruolo
    director_keywords = ["diretto da", "regia di", "film di", "serie di", "serie tv di", "di" ,"diretti da"]
    actor_keywords = ["con", "nel cast", "starring", "attore", "attrice", "interpretato da", "interpretata da", "interpreti", "attori", "attrici"]
    # Cerchiamo la parola chiave con il match più alto per ogni ruolo
    director_match = process.extractOne(preceding_text, director_keywords, score_cutoff=95)
    actor_match = process.extractOne(preceding_text, actor_keywords, score_cutoff=95)
    # Determiniamo il ruolo basato sul match con il punteggio più alto
    if director_match and (not actor_match or director_match[1] > actor_match[1]):
        return "regista"
    elif actor_match:
        return "attore"
    return None

def infer_roles_for_all_entities(text: Text, entities: List[Dict[Text, Any]]) -> Dict[Text, Text]:
    roles = {}
    for entity in entities:
        if entity['entity'] == 'persona':
            # Uniamo nomi spezzati, assumendo che l'entity recognizer possa averli divisi
            full_name = merge_split_names(text, entity)
            role = infer_role_from_context(text, entity['start'])
            roles[full_name] = role
    return roles

def merge_split_names(text: Text, entity: Dict) -> Text:
    end_pos = entity['end']
    if end_pos < len(text) and text[end_pos] == ' ':  # Se l'entità è seguita da uno spazio
        match = re.search(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', text[end_pos:])
        if match:
            return match.group(0)
    return entity['value']

class ActionRicercaContenuti(Action):
    def name(self) -> Text:
        return "action_ricerca_contenuti"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        df = pd.read_csv(PATH_TO_CSV, converters={"genres_list": ast.literal_eval})
        entita_riconosciute = tracker.latest_message['entities']
        
        query = {}  # Dizionario per costruire la query di ricerca
        tipo_specified = None
        # Usa la funzione migliorata per inferire i ruoli di tutte le entità 'persona'
        roles = infer_roles_for_all_entities(tracker.latest_message['text'], entita_riconosciute)
        
        for entita in entita_riconosciute:
            if entita['entity'] == 'tipo':
                tipo_valori = ['film', 'movie', 'titolo', 'pellicola', 'serie', 'tv show', 'tv serie', 'telefilm', 'programma tv', 'serie tv', 'show', 'programma']
                matched_type = process.extractOne(entita['value'].lower(), tipo_valori, scorer=fuzz.token_set_ratio)
                if matched_type[1] > 90:
                    tipo_specified = 'Movie' if matched_type[0] in ['film', 'movie', 'titolo', 'pellicola'] else 'TV Show'
                    query['type'] = tipo_specified
            
            elif entita['entity'] == 'persona':
                # Utilizziamo il ruolo inferito dalla funzione migliorata
                role = roles.get(entita['value'], None)
                query_value = entita['value'].lower()
                columns_to_search = []
                if role == 'attore':
                    columns_to_search = ['cast']
                    print("attore")
                elif role == 'regista':
                    columns_to_search = ['director']
                    print("regista")
                else:
                    columns_to_search = ['cast', 'director']
                final_match = None
                highest_score = 0
                final_column = None
                for column in columns_to_search:
                    search_list = df[column].str.split(', ').explode().unique()
                    match = process.extractOne(query_value, search_list, score_cutoff=95)
                    if match and match[1] > highest_score:
                        highest_score = match[1]
                        final_match = match[0]
                        final_column = column  
                if final_match and final_column:
                    df = df[df[final_column].str.contains(final_match, case=False, na=False)]
                    query[final_column] = final_match
                else:
                    dispatcher.utter_message(text="Non ho trovato risultati corrispondenti alla tua ricerca.")
                    return []
                
            elif entita['entity'] == 'genere':
                matched_genres = []  # Lista per tenere traccia dei generi corrispondenti
                # Verifica se il tipo è specificato e se è 'Movie'
                if tipo_specified == 'Movie':
                    matched_genre = trova_corrispondenza(entita['value'], mappatura_generi_film)
                    if matched_genre:
                        matched_genres.append(matched_genre)
                # Verifica se il tipo è specificato e se è 'TV Show'
                elif tipo_specified == 'TV Show':
                    matched_genre = trova_corrispondenza(entita['value'], mappatura_generi_serie_tv)
                    if matched_genre:
                        matched_genres.append(matched_genre)
                # Se il tipo non è specificato, cerca in entrambi (film e serie TV)
                else:
                    matched_genre_film = trova_corrispondenza(entita['value'], mappatura_generi_film)
                    if matched_genre_film:
                        matched_genres.append(matched_genre_film)

                    matched_genre_serie = trova_corrispondenza(entita['value'], mappatura_generi_serie_tv)
                    if matched_genre_serie:
                        matched_genres.append(matched_genre_serie)
                if matched_genres:
                    query['genres_list'] = matched_genres
            
            
            elif entita['entity'] == 'paese':
                matched_country = trova_corrispondenza(entita['value'], mappatura_paesi)
                if matched_country:
                    query['country'] = matched_country
            
            
            elif entita['entity'] == 'categoria':
                matched_category = trova_corrispondenza(entita['value'], mappatura_categorie)
                if matched_category:
                    query['rating_category'] = matched_category
            
            
            elif entita['entity'] == 'anno':
                query['release_year'] = int(entita['value'])
            
            
            elif entita['entity'] == 'durata':
                # Estrazione del numero e dell'unità dalla durata
                durata_match = re.search(r'(\d+)\s*(minuti|stagioni|stagione|min)', entita['value'], re.IGNORECASE)
                if durata_match:
                    numero, unita = durata_match.groups()
                    if 'min' in unita.lower() or 'minuti' in unita.lower():
                        query['duration_number'] = int(numero)
                        query['duration_unit'] = 'min'
                    else:
                        query['duration_number'] = int(numero)
                        if  int(numero) == 1:
                            query['duration_unit'] = 'season'
                        else:
                            query['duration_unit'] = 'seasons'

        # Applica i filtri basati sulla query costruita dalle entità
        for key, value in query.items():
            if key == 'genres_list':
                # Crea una condizione per il filtro basata sui generi
                genre_condition = df['genres_list'].apply(lambda genres: any(genre in query['genres_list'] for genre in genres))
                # Se il tipo è specificato, usa anche il filtro per tipo
                if 'type' in query:
                    df = df[(df['type'] == query['type']) & genre_condition]
                else:
                    # Se il tipo non è specificato, ignora il filtro per tipo e utilizza solo quello per genere
                    df = df[genre_condition]
            
            elif key == 'country':
                df = df[df['country'].str.contains(value, case=False, na=False)]
            
            elif key == 'rating_category':
                df = df[df['rating_category'] == value]
            
            elif key == 'type':
                df = df[df['type'] == value]
            
            elif key == 'release_year':
                df = df[df['release_year'] == int(value)]
            
            elif key == 'duration_number':
                # Gestione della durata per i film
                if 'duration_unit' in query and query['duration_unit'] == 'min':
                    df = df[(df['type'] == 'Movie') & (df['duration_number'] <= int(value))]
                # Gestione delle stagioni per le serie TV
                elif 'duration_unit' in query and query['duration_unit'] != 'min':
                    df = df[(df['type'] == 'TV Show') & (df['duration_number'] <= int(value))]
        
        # Invio dei risultati
        if df.empty:
            dispatcher.utter_message(text="Non ho trovato risultati corrispondenti alla tua ricerca.")
        else:
            shuffled_results = df.sample(frac=1).reset_index(drop=True)  # Mescola i risultati
            risultati = shuffled_results.head(20) # 20 titoli massimi
            intro = "Ecco i risultati trovati"  # Messaggio di default

            if 'type' in query:
                if query['type'] == 'Movie':
                    intro = "Ecco i film trovati"
                elif query['type'] == 'TV Show':
                    intro = "Ecco le serie trovate"
            
            if 'cast' in query:
                intro += f" con {query['cast'].title()}"
            
            if 'director' in query:
                intro += f" diretti da {query['director'].title()}"

            # Costruzione del messaggio di risposta con l'intro modificato
            filtri_applicati = []
            for k, v in query.items():
                if k == 'type':
                    continue
                elif k == 'genres_list':
                    filtri_applicati.append(f"# Genere/i: {', '.join([g.title() for g in v])}")
                elif k == 'duration_number':
                    if query['duration_unit'] == 'min':
                        filtri_applicati.append(f"# Durata massima: {v} min")
                    else:
                        if v == 1:
                            filtri_applicati.append(f"# Durata massima: {v} stagione")
                        else:
                            filtri_applicati.append(f"# Durata massima: {v} stagioni")
                elif k == 'release_year':
                    filtri_applicati.append(f"# Anno di uscita: {v}")
                elif k == 'rating_category':
                    filtri_applicati.append(f"# Categoria di visione: {v}")
                elif k in ['attore', 'regista']:
                    filtri_applicati.append(f"{k}: {v.title()}")
                else:
                    filtri_applicati.append(f"{k}: {str(v).title()}")

            if filtri_applicati:
                intro += f" con i seguenti filtri:\n{', '.join(filtri_applicati)}.\n"

            risposta = f"{intro}\n\n"
            for index, row in risultati.iterrows():
                titolo = row['title'].title()
                tipo = row['type']
                descrizione = row['description']
                regista = row['director']
                cast = row['cast']
                categoria = row['rating_category']
                if tipo == 'Movie':
                    durata = f"{row.get('duration_number', 'N/D')} min" if 'duration_number' in row else 'N/D'
                else:
                    durata = f"{row.get('duration_number', 'N/D')} stagione/i" if 'duration_number' in row else 'N/D'
                risposta += f"\n- {titolo} ({'Film' if tipo == 'Movie' else 'Serie TV'}, Durata massima: {durata}):\n   Descrizione: {descrizione}\n   Regia: {regista}\n   Cast: {cast}\n   Categoria di pubblico: {categoria}\n   Genere/i: {', '.join(row['genres_list'])}\n\n"

            dispatcher.utter_message(text=risposta)
            
            return []



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
        

class ResetSlot(Action):
    def name(self):
        return "action_reset_slots"

    def run(self,
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(text="Ora puoi chiedermi qualcos'altro!")
        return [AllSlotsReset()]
    
# Azione per ottenere i paesi dai dati   
class GetPaesiFromData(Action):

    def name(self) -> Text:
        return "action_get_paesi_from_data"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Carica il dataset
        df = pd.read_csv(PATH_TO_CSV)

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

# Azione per ottenere le categorie dai dati
class ActionGetCategorieFromMap(Action):
    
        def name(self) -> Text:
            return "action_get_categorie_from_map"
    
        def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            # Estraiamo le categorie dalla mappatura delle categorie
            categorie = list(mappatura_categorie.keys())
    
            # Creiamo la stringa per l'output, mettendo ogni categoria su una nuova linea
            categorie_message = "- " + "\n- ".join(categorie)
    
            # Creo il messaggio da inviare all'utente
            messaggio = "Ecco alcune categorie che potresti cercare:\n\n" + categorie_message
    
            # Invio il messaggio
            dispatcher.utter_message(text=messaggio)
    
            return []

# Azione per ottenere informazioni sul contenuto passato
class ActionGetInfoFromTitle(Action):

    def name(self) -> Text:
        return "action_informazioni_contenuto"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        df = pd.read_csv(PATH_TO_CSV)
        
        text = tracker.latest_message.get('text')  # Ottiene il testo completo del messaggio
        # Isola il titolo dalla richiesta dell'utente
        isolated_title = isolate_title_from_request(text)

        # Usa fuzzy matching per trovare il titolo più simile nel dataset
        titles = df['title'].tolist()
        best_match, score = process.extractOne(isolated_title, titles)
        
        if score > 90:  # Soglia di accettazione per il fuzzy matching
            result = df[df['title'].str.lower() == best_match.lower()]
                
            if not result.empty:
                tipo = result.iloc[0]['type']
                descrizione = result.iloc[0]['description']
                regista = "Non specificato" if pd.isnull(result.iloc[0]['director']) else result.iloc[0]['director']
                cast = "Non specificato" if pd.isnull(result.iloc[0]['cast']) else result.iloc[0]['cast']
                categoria = result.iloc[0]['rating_category']
                generi = ast.literal_eval(result.iloc[0]['genres_list']) if pd.notna(result.iloc[0]['genres_list']) else ["Non specificato"]
                titolo = result.iloc[0]['title']

                messaggio = f"- {titolo} è un {'Film' if tipo == 'Movie' else 'Serie TV'} con le seguenti informazioni:\n\n"
                messaggio += f"   Descrizione: {descrizione}\n"
                messaggio += f"   Regia: {regista}\n"
                messaggio += f"   Cast: {cast}\n"
                messaggio += f"   Categoria di pubblico: {categoria}\n"
                messaggio += f"   Genere/i: {', '.join(generi)}"

                dispatcher.utter_message(text=messaggio)
            else:
                dispatcher.utter_message(text=f"Non ho trovato informazioni per il titolo '{titolo}'.")
        else:
            dispatcher.utter_message(text="Non ho potuto identificare il titolo nella tua richiesta.")

        return []
    


# Parte della gestione della FORM per i consigli di contenuti
logger = logging.getLogger(__name__)
# Action per validate FORM consigli contenuti solo per tipo e per titolo
class ValidateConsigliContenutiForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_consigliare_contenuto_form"

    def validate_tipo(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        tipo_contenuto = tracker.get_slot('tipo').lower()
        logger.debug(f"Validating slot 'tipo' with value '{tipo_contenuto}'")
        
        if tipo_contenuto in ["film", "serie", "serie tv", "movie", "tv show", "show"]:
            if tipo_contenuto in ["film", "movie"]:
                return {"tipo": "Movie"}
            elif tipo_contenuto in ["serie", "serie tv", "tv show", "show"]:
                return {"tipo": "TV Show"}
        else:
            dispatcher.utter_message(text="Per favore, scegli una delle opzioni disponibili: 'Film' o 'Serie'.")
            return {"tipo": None}

    def validate_titolo(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        titolo = tracker.get_slot('titolo').lower()
        logger.debug(f"Validating slot 'titolo' with value '{titolo}'")

        try:
            df = pd.read_csv(PATH_TO_CSV) # Aggiorna con il percorso corretto
            titles = df['title'].str.lower().tolist()
            best_match, score = process.extractOne(titolo, titles)
        except Exception as e:
            logger.error(f"Error reading CSV or validating title: {e}")
            dispatcher.utter_message(text="Si è verificato un errore nella validazione del titolo.")
            return {"titolo": None}

        if score > 90:
            return {"titolo": best_match}
        else:
            dispatcher.utter_message(text="Non ho trovato il titolo che hai inserito, potremmo non averlo in catalogo. Puoi riprovare?")
            return {"titolo": None}

# Azione per la sottomissione della form di consiglio sui contenuti.
# Questa azione raccoglie gli slot compilati dall'utente durante la sessione della form.
# Gli slot raccolti vengono utilizzati per eseguire una ricerca personalizzata nel dataset.
# In particolare, il titolo fornito dall'utente viene impiegato per estrarre dettagli chiave
# relativi al contenuto, quali il cast, il regista e i generi associati.
# Successivamente, questi elementi vengono utilizzati come filtri per identificare e suggerire
# film o serie TV che condividono almeno uno di questi attributi con il titolo di riferimento.
# Il processo risulta quindi in una raccolta curata di contenuti che presentano similitudini
# significative con le preferenze espresse dall'utente tramite il titolo indicato.
# Nel caso in cui la ricerca non produca risultati, viene notificato all'utente
# tramite un messaggio che indica l'impossibilità di trovare contenuti corrispondenti ai criteri specificati.
class SubmitConsigliareContenutoForm(Action):
    def name(self) -> Text:
        return "action_submit_consigliare_contenuto_form"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        df = pd.read_csv(PATH_TO_CSV)
        slot_values = tracker.slots

        # Estraiamo il titolo dallo slot
        title = slot_values['titolo']
        # Estraiamo il tipo dallo slot
        tipo = slot_values['tipo']
        
        titles = df['title'].tolist()
        best_match, score = process.extractOne(title, titles)
        if score > 90:
            result = df[df['title'].str.lower() == best_match.lower()]

        if not result.empty:
            # Estraiamo i dettagli relativi al titolo selezionato
            cast = result.iloc[0]['cast'].split(", ")
            director = result.iloc[0]['director']
            genres = ast.literal_eval(result.iloc[0]['genres_list'])

            # Prepariamo i filtri basati su cast e director
            cast_filter = df['cast'].apply(lambda x: any(actor in x for actor in cast if x != 'Non disponibile'))
            director_filter = df['director'].str.contains(director, case=False, na=False)
            genres_filter = df['genres_list'].apply(lambda x: any(genre in ast.literal_eval(x) for genre in genres if x))

            if tipo == 'Movie':
                similar_content = df[(df['title'].str.lower() != best_match.lower()) & 
                                     (df['type'] == 'Movie') & 
                                     (cast_filter | director_filter | genres_filter)]
            elif tipo == 'TV Show':
                similar_content = df[(df['title'].str.lower() != best_match.lower()) & 
                                     (df['type'] == 'TV Show') & 
                                     (cast_filter | director_filter | genres_filter)]

            if not similar_content.empty:
                shuffled_results = similar_content.sample(frac=1).reset_index(drop=True)
                results = shuffled_results.head(30) # ridai 30 titoli per semplicita'
                intro = f"Ecco alcuni contenuti simili a '{title}':\n\n"
                risposta = intro
                for index, row in results.iterrows():
                    titolo = row['title'].title()
                    tipo = row['type']
                    descrizione = row['description']
                    regista = row['director']
                    cast = row['cast']
                    categoria = row['rating_category']
                    generi = ast.literal_eval(row['genres_list']) if pd.notna(row['genres_list']) else ["Non specificato"]
                    risposta += f"\n- {titolo} ({'Film' if tipo == 'Movie' else 'Serie TV'}):\n   Descrizione: {descrizione}\n   Regia: {regista}\n   Cast: {cast}\n   Categoria di pubblico: {categoria}\n   Genere/i: {', '.join(generi)}\n\n"
                similar_content.to_csv("actions/risultati_consigliati.csv", index=False)
                dispatcher.utter_message(text=risposta)
            else:
                dispatcher.utter_message(text=f"Non ho trovato contenuti simili a '{title}'.")
        else:
            dispatcher.utter_message(text=f"Non ho trovato informazioni per il titolo '{title}'.")
        return []