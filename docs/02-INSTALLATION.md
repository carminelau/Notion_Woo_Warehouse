````markdown
# 📥 Installazione e Configurazione

## 🚀 Installazione Rapida

### 1. Clone/Estrai il progetto
```bash
cd c:\Work\Docker_Stock_management
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

## 🔧 Setup Dettagliato

### WooCommerce Setup

1. **Accedi al dashboard WooCommerce**
   - Vai su `tuostore.com/wp-admin`
   - Accedi con credenziali admin

2. **Attiva le API REST**
   - Vai a **WooCommerce → Impostazioni → API**
   - Legge il token di API automaticamente generato

3. **Crea una nuova Key API**
   - Clicca **Create an application**
   - Nome: `Stock Management Sync`
   - Descrizione: `Sincronizzazione automatica stock con Notion`
   - User: Seleziona un admin user
   - Permissions: **Read/Write** (necessario per update stock)
   - Clicca **Create**

4. **Copia le credenziali**
   ```env
   WOOCOMMERCE_API_URL=https://tuostore.com
   WOOCOMMERCE_CONSUMER_KEY=ck_xxxxxxxxxxxxxxxx
   WOOCOMMERCE_CONSUMER_SECRET=cs_xxxxxxxxxxxxxxxx
   ```

### Notion Setup

1. **Accedi a Notion**
   - Vai su https://www.notion.so

2. **Crea una nuova integrazione**
   - Vai su **My integrations**
   - Clicca **Create new integration**
   - Nome: `Stock Management Sync`
   - Logo: (opzionale)
   - Capabilities: `Read`, `Update`, `Insert` content
   - Clicca **Submit**

3. **Copia il token**
   - Clicca **Show**
   - Copia il token segreto
   ```env
   NOTION_TOKEN=secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

4. **Crea il database**
   - Vedi **03-NOTION_SETUP.md** per dettagli

5. **Ottieni Database ID**
   - Apri il database in browser
   - URL: `https://www.notion.so/workspace/xxxxxxxxxxxxxxxxxxxxx?v=yyy`
   - ID = `xxxxxxxxxxxxxxxxxxxxx`
   ```env
   NOTION_DATABASE_ID=xxxxxxxxxxxxxxxxxxxxx
   ```

6. **Condividi database con integrazione**
   - Apri il database
   - Clicca **Share**
   - Seleziona la tua integrazione
   - Scegli **Editor**
   - Salva

## 🐳 Docker Configuration

### Dockerfile
```dockerfile
FROM python:3.11-slim

# Installa dipendenze di sistema
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Imposta directory di lavoro
WORKDIR /app

# Copia file di progetto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Comandi
CMD ["python", "main.py"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  stock-sync:
    build:
      context: .
      dockerfile: Dockerfile
    
    container_name: stock-sync
    
    env_file: .env
    
    environment:
      - PYTHONUNBUFFERED=1
    
    volumes:
      - ./logs:/app/logs
      - ./config:/app/config
    
    restart: unless-stopped
    
    networks:
      - stock-network

networks:
  stock-network:
    driver: bridge
```

## 📁 Struttura Progetto

```
Docker_Stock_management/
├── Dockerfile              # Configurazione container
├── docker-compose.yml      # Orchestrazione servizi
├── requirements.txt        # Dipendenze Python
├── main.py                 # Script principale
├── sync/
│   ├── __init__.py
│   ├── woocommerce_client.py   # Client WooCommerce
│   ├── notion_client.py        # Client Notion
│   ├── stock_sync.py           # Logica sincronizzazione
│   ├── ai_agent.py             # 🤖 AI Agent
│   └── notifier.py             # 📢 Notifiche
├── logs/                   # Log della sincronizzazione
├── config/                 # Configurazioni
├── docs/                   # 📚 Documentazione
├── scripts/                # 🔧 Script utility
├── .env                    # ⚠️ Variabili ambiente (privato)
├── .env.example            # Template .env
├── .gitignore              # File da ignorare
├── README.md               # 📌 Leggi prima
├── Makefile                # Comandi veloci
└── package.json            # Metadati progetto
```

## ✅ Checklist Installazione

- [ ] Clonato/estratto il progetto
- [ ] Copiato `.env.example` in `.env`
- [ ] Ottenute credenziali WooCommerce API
- [ ] Configurato `WOOCOMMERCE_API_URL` in `.env`
- [ ] Configurato `WOOCOMMERCE_CONSUMER_KEY` in `.env`
- [ ] Configurato `WOOCOMMERCE_CONSUMER_SECRET` in `.env`
- [ ] Creato database Notion (vedi **03-NOTION_SETUP.md**)
- [ ] Configurato `NOTION_TOKEN` in `.env`
- [ ] Configurato `NOTION_DATABASE_ID` in `.env`
- [ ] Costruito container: `docker-compose build`
- [ ] Avviato sistema: `docker-compose up -d`
- [ ] Verificati log: `docker-compose logs -f`

## 🧪 Test Installazione

### Verifica Docker
```bash
docker --version
docker-compose --version
```

### Verifica Python (se locale)
```bash
python --version
pip --version
```

### Verifica Dipendenze
```bash
pip install -r requirements.txt
```

### Verifica Connessioni
```bash
# Test WooCommerce
curl https://tuostore.com/wp-json/wc/v3/products \
  -H "Authorization: Basic $(echo -n 'key:secret' | base64)"

# Test Notion
curl https://api.notion.com/v1/databases/xxxxx \
  -H "Authorization: Bearer secret_xxxxx"
```

### Test Locale (no Docker)
```bash
python test_ai_agent.py
```

## 🚨 Troubleshooting Installazione

### Errore: "Port 8080 already in use"
```bash
# Usa una porta diversa
docker-compose -e "PORT=8081" up -d
```

### Errore: "Cannot connect to Docker daemon"
```bash
# Assicurati che Docker sia avviato
# Windows: Avvia Docker Desktop
# Linux: sudo systemctl start docker
```

### Errore: "Module not found"
```bash
# Ricostruisci il container
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Errore: "Invalid credentials"
```bash
# Verifica che .env contiene credenziali corrette
# Ricarica le variabili di ambiente:
docker-compose restart
```

### API non funziona
```bash
# Verifica connessione
docker-compose logs stock-sync | grep "ERROR"

# Test manuale
docker-compose exec stock-sync python -c "
from sync.woocommerce_client import WooCommerceClient
woo = WooCommerceClient()
print(woo.get_products())
"
```

## 📞 Supporto

Per ulteriore aiuto:
- Leggi **01-QUICK_START.md**
- Consulta **04-AI_AGENT.md**
- Esegui `docker-compose logs -f` per debugging

````
