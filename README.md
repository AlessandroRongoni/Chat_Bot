# ChatBot di Netflix

Il ChatBot di Netflix è un progetto innovativo realizzato per il corso di Data Science presso l'Università Politecnica delle Marche. Questo strumento è stato sviluppato per ottimizzare l'esperienza degli utenti nella ricerca e scoperta di contenuti sulla piattaforma Netflix. Sfruttando le capacità del framework Rasa, il chatbot implementa una serie di comandi interattivi che consentono ricerche dettagliate e forniscono raccomandazioni personalizzate basate sulle preferenze degli utenti. La combinazione di tecnologie avanzate di analisi dei dati e intelligenza artificiale rende questo chatbot particolarmente efficace nel comprendere e anticipare le necessità degli utenti, facilitando un'esperienza utente più coinvolgente e soddisfacente.



<p align="center">
  <img src="img/logo_chatbot.png" alt="Logo del Progetto" width="300" height="300"/>
</p>

## Indice

- [Introduzione](#chatbot-di-netflix)
- [Funzionalità](#funzionalità)
- [Tecnologie Utilizzate](#tecnologie-utilizzate)
- [Dataset](#dataset)
- [Installazione](#installazione)
- [Licenza](#licenza)
- [Autori](#autori)
- [Contribuire](#contribuire)

## Funzionalità

Il ChatBot di Netflix supporta le seguenti funzionalità:

- **Ricerca per Attore**: Trova tutti i film o le serie TV in cui un dato attore ha recitato.
- **Ricerca per Regista**: Scopri opere dirette da un particolare regista.
- **Ricerca per Genere**: Filtra i contenuti per genere, come azione, dramma, commedia, ecc.
- **Ricerca per Anno**: Ricerca contenuti rilasciati in un specifico anno.
- **Ricerca per Categoria**: Esplora contenuti basati su categorie come film per famiglie, thriller, documentari, ecc.
- **Informazioni per Titolo**: Ottieni dettagli specifici su un titolo, inclusi cast, durata, sinossi e valutazione.
- **Ricerca per Durata**: Cerca contenuti filtrando per durata del film o episodi.
- **Ricerca per Tipo di Contenuto**: Distingui tra film e serie TV.
- **Ricerca per Paese**: Trova contenuti prodotti in specifici paesi.
- **Consigli di Visione**: Ricevi raccomandazioni basate sulle tue preferenze di visualizzazione precedenti.
- **Generi Disponibili**: Ottieni una lista dei generi disponibili su Netflix.
- **Paesi Disponibili**: Scopri l'elenco dei paesi di produzione dei contenuti disponibili.
- **Categorie Disponibili**: Visualizza le categorie di contenuti che puoi esplorare.

## Tecnologie Utilizzate

- **Rasa**: Un framework open source per la costruzione di chatbot e assistenti virtuali.
- **Pandas**: Una libreria di Python utilizzata per la manipolazione e l'analisi dei dati.
- **FuzzyWuzzy**: Una libreria Python che viene utilizzata per la ricerca di corrispondenze approssimate tra stringhe.

## Dataset
Il dataset "Netflix Movies and TV Shows" su Kaggle contiene informazioni dettagliate sui contenuti disponibili su Netflix. Questo dataset è utilizzato per analizzare e visualizzare le tendenze dei media su Netflix.

### Struttura del Dataset

Il dataset include le seguenti colonne:

- `show_id`: Identificativo unico per ciascun titolo.
- `type`: Tipo del contenuto, che può essere "Movie" o "TV Show".
- `title`: Titolo del film o della serie.
- `director`: Regista del film o della serie.
- `cast`: Attori coinvolti.
- `country`: Paese di produzione.
- `date_added`: Data di aggiunta su Netflix.
- `release_year`: Anno di uscita del contenuto.
- `rating`: Classificazione del contenuto.
- `duration`: Durata del film o numero di stagioni per le serie.
- `listed_in`: Generi del contenuto.
- `description`: Breve descrizione del contenuto.

### Utilizzo del Dataset

Dopo aver scaricato il dataset da Kaggle, puoi utilizzare Python e Pandas per caricare e analizzare i dati. Qui sotto trovi un esempio di come caricare il dataset e eseguire alcune query di base.

```python
import pandas as pd

# Carica il dataset
df = pd.read_csv('path/to/netflix-shows.csv')

# Visualizza le prime righe del DataFrame
print(df.head())

# Esempi di query semplici
# Trova tutti i film rilasciati nel 2020
movies_2020 = df[(df['type'] == 'Movie') & (df['release_year'] == 2020)]
print(movies_2020)

# Conta il numero di show per ogni paese
country_counts = df['country'].value_counts()
print(country_counts)

# Filtra per titoli con una specifica parola chiave nella descrizione
keyword_filter = df[df['description'].str.contains('love', na=False)]
print(keyword_filter)
```
#### Link al dataset: [Netflix Movies and TV Shows Dataset on Kaggle](https://www.kaggle.com/datasets/shivamb/netflix-shows)

## Installazione

Per iniziare a utilizzare il ChatBot di Netflix, segui questi passi per configurare l'ambiente e installare le dipendenze necessarie:

```bash
# Clona il repository
git clone https://github.com/AlessandroRongoni/Chat_Bot
cd Chat_Bot

# Crea un ambiente virtuale
python -m venv venv
source venv/bin/activate

# Installa le dipendenze
pip install -r requirements.txt

# Avvia il server Rasa
rasa train
rasa run
rasa run actions
```
## Licenza

Questo progetto è rilasciato sotto la [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html), una licenza pubblica molto permissiva che permette la modifica, l'uso e la distribuzione del software, purché tutte le copie e le versioni modificate siano anch'esse disponibili sotto la stessa licenza.

Per maggiori dettagli sulla licenza, si prega di consultare il testo completo della licenza a questo link: [GNU GPL v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html).

## Autori

Questo progetto è stato creato da:

- **Alessandro Rongoni** - *Developer* - [AlessandroRongoni](https://github.com/AlessandroRongoni)
- **Vito Scaraggi** - *Developer* - [Vito-Scaraggi](https://github.com/Vito-Scaraggi)
- **Christopher Buratti** - *Developer* - [christopherburatti](https://github.com/christopherburatti)
- **Luca Guidi** - *Developer* - [LucaGuidi5](https://github.com/LucaGuidi5)
