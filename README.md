# Notion_Woo_Warehouse

Sistema di sincronizzazione automatico dello stock tra **WooCommerce** e **Notion** tramite container Docker.

## 📚 Documentazione Completa

Leggi la documentazione nella cartella **`docs/`**:

- **[01-QUICK_START.md](docs/01-QUICK_START.md)** - ⚡ Guida rapida (inizia da qui!)
- **[02-INSTALLATION.md](docs/02-INSTALLATION.md)** - 📥 Installazione completa passo per passo
- **[03-NOTION_SETUP.md](docs/03-NOTION_SETUP.md)** - 📋 Setup database Notion dettagliato
- **[04-AI_AGENT.md](docs/04-AI_AGENT.md)** - 🤖 API tecnica e esempi codice
- **[05-CHANGELOG.md](docs/05-CHANGELOG.md)** - 📝 Novità versione 2.0.0
- **[06-STRUCTURE.md](docs/06-STRUCTURE.md)** - 📁 Struttura progetto completa
- **[07-CONTRIBUTING.md](docs/07-CONTRIBUTING.md)** - 👥 Come contribuire a GitHub

## 📋 Caratteristiche

- ✅ Sincronizzazione bidirezionale dello stock
- ✅ Supporto per SKU come identificatore unico
- ✅ Aggiornamento automatico e periodico
- ✅ Logging dettagliato con traccia degli errori
- ✅ Facile configurazione via variabili di ambiente
- ✅ Container Docker isolato e replicabile
- ✅ **AI Agent Intelligente** 🤖
  - Rilevamento automatico discrepanze di stock
  - Analisi anomalie prodotti
  - Suggerimenti intelligenti di riordino
  - Report analitici con insights
  - Monitoraggio proattivo dello stock

## 🚀 Installazione Rapida

### 1. Clone/Estrai il progetto
```bash
cd c:\Work\Notion_Woo_Warehouse
```

### 2. Copia il file di configurazione
```bash
cp .env.example .env
```

### 3. Configura le credenziali nel file `.env`

#### Per WooCommerce:
1. Accedi alla tua store WooCommerce
2. Vai a **Impostazioni > API**
3. Crea una nuova applicazione API
4. Copia i valori di:
   - **URL API**: `https://tuostore.com`
   - **Consumer Key**
   - **Consumer Secret**

#### Per Notion:
1. Vai su https://www.notion.so/my-integrations
2. Crea una nuova integrazione
3. Copia il **token di integrazione** (interno segreto)
4. Condividi il tuo database con l'integrazione
5. Copia l'ID del database dall'URL

### 4. Costruisci e avvia il container

#### Con Docker Compose (consigliato):
```bash
docker-compose up -d
```

#### Con Docker diretto:
```bash
docker build -t stock-management .
docker run -d --name stock-sync --env-file .env stock-management
```

## � Struttura del Progetto

```
Docker_Stock_management/
├── Dockerfile              # Configurazione container
├── docker-compose.yml      # Orchestrazione servizi
├── requirements.txt        # Dipendenze Python
├── main.py                 # Script principale
├── sync/
│   ├── __init__.py
│   ├── woocommerce_client.py   # Client WooCommerce API
│   ├── notion_client.py        # Client Notion API
│   ├── stock_sync.py           # Logica di sincronizzazione
│   ├── ai_agent.py             # 🤖 AI Agent intelligente
│   └── notifier.py             # 📢 Notifiche e report
├── logs/                   # Log della sincronizzazione
├── config/                 # Configurazioni aggiuntive
├── .env.example            # Variabili di ambiente (template)
└── README.md              # Questo file
```

## ⚙️ Variabili di Ambiente

| Variabile | Descrizione | Esempio |
|-----------|-------------|---------|
| `WOOCOMMERCE_API_URL` | URL della store WooCommerce | `https://mystore.com` |
| `WOOCOMMERCE_CONSUMER_KEY` | Chiave consumer API WooCommerce | `ck_xxxxx` |
| `WOOCOMMERCE_CONSUMER_SECRET` | Secret consumer API WooCommerce | `cs_xxxxx` |
| `NOTION_TOKEN` | Token integrazione Notion | `secret_xxxxx` |
| `NOTION_DATABASE_ID` | ID del database Notion | `xxxxx-xxxxx` |
| `SYNC_INTERVAL` | Intervallo sincronizzazione in secondi | `300` (5 minuti) |
| `LOG_LEVEL` | Livello di logging | `INFO` |
| `AI_MODEL` | Modello AI da usare | `local` |
| `STOCK_WARNING_THRESHOLD` | Soglia unità per avviso stock basso | `10` |

## 🔄 Come Funziona la Sincronizzazione

### Flusso Bidirezionale:
1. **WooCommerce → Notion**: Legge i prodotti da WooCommerce e aggiorna gli stock in Notion
2. **Notion → WooCommerce**: Legge gli item da Notion e aggiorna i prodotti in WooCommerce

### Identificazione:
- Usa lo **SKU** come campo di collegamento tra i due sistemi
- Assicurati che SKU sia presente in entrambi i sistemi

### Proprietà Notion Richieste:
- `Name` (Title): Nome del prodotto
- `SKU` (Rich Text): Codice SKU univoco
- `Stock` (Number): Quantità di stock

## 🤖 Capacità AI Agent

Il sistema integra un **AI Agent intelligente** che fornisce:

### 1. **Rilevamento Discrepanze** 🔍
- Identifica automaticamente differenze di stock tra WooCommerce e Notion
- Calcola il livello di gravità (LOW, MEDIUM, HIGH, CRITICAL)
- Genera avvisi dettagliati

### 2. **Analisi Anomalie** ⚠️
Rileva automaticamente:
- **Stock negativo** (CRITICAL) - Errore di sincronizzazione
- **Prodotti esauriti** ma ancora attivi (HIGH)
- **Prezzi mancanti** (MEDIUM)
- **Stock insoliti** (MEDIUM) - Possibili errori

### 3. **Suggerimenti di Riordino** 💡
- Identifica prodotti sotto soglia di stock
- Suggerisce quantità di riordino intelligente
- Calcola urgenza (CRITICAL, HIGH, MEDIUM)

### 4. **Report Analitici** 📊
Genera report che includono:
- Stock medio per categoria
- Numero prodotti esauriti
- Tasso di sincronizzazione
- Statistiche e trends

### 5. **Notifiche Intelligenti** 📢
- Alert in tempo reale su anomalie critiche
- Suggerimenti di riordino prioritizzati
- Summary report periodico

## 📊 Log e Monitoraggio

I log vengono salvati in `logs/stock_sync.log`:

```bash
# Visualizza i log in tempo reale
docker-compose logs -f stock-sync

# Visualizza gli ultimi 100 righe
docker logs stock-sync --tail=100 -f
```

## 🐛 Troubleshooting

### Errore: "Connection refused"
- Verifica che WooCommerce sia raggiungibile
- Controlla l'URL nei parametri di configurazione

### Errore: "Invalid credentials"
- Controlla Consumer Key e Consumer Secret
- Assicurati che l'API sia abilitata in WooCommerce

### Errore: "Notion token invalid"
- Verifica il token nel file `.env`
- Ricrea l'integrazione Notion se necessario

### Sincronizzazione non avviene
- Controlla il log: `docker-compose logs`
- Verifica che gli SKU siano presenti in entrambi i sistemi
- Aumenta il livello di logging: `LOG_LEVEL=DEBUG`

## 🔐 Sicurezza

- **NON** committare il file `.env` con credenziali reali
- Usa `.env.example` come template
- Le credenziali dovrebbero essere gestite tramite secrets manager
- Considera l'uso di un proxy inverso per HTTPS

## 📝 Configurazione Avanzata

### Aggiungere Campi Personalizzati
Modifica il mapping delle proprietà in `sync/stock_sync.py`:

```python
# Esempi di estrazione proprietà
sku = self.notion.extract_property(item, 'SKU')
price = self.notion.extract_property(item, 'Price')
category = self.notion.extract_property(item, 'Category')
```

### Sincronizzazione Filtrata
Modifica `_sync_woo_to_notion()` e `_sync_notion_to_woo()` per filtrare prodotti/item:

```python
# Esempio: sincronizza solo prodotti attivi
if not product.get('status') == 'publish':
    continue
```

## 🛠️ Sviluppo Locale

### Requisiti
- Python 3.11+
- Docker e Docker Compose

### Setup locale (senza Docker):
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt
python main.py
```

## 📄 Licenza

Questo progetto è fornito così com'è per uso interno.

## 💡 Suggerimenti

- Esegui una sincronizzazione iniziale in modalità DEBUG
- Testa con prodotti/item di prova prima di andare in produzione
- Configura backup del database Notion
- Monitora i log per identificare discrepanze di stock

## 📞 Support

Per problemi o suggerimenti, controlla i log dettagliati con:
```bash
docker-compose logs -f stock-sync
```
