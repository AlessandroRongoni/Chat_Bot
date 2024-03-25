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
