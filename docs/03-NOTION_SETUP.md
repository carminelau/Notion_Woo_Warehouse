````markdown
# 📋 Guida Setup Database Notion

## 🎯 Configurazione Campi Notion

Quando crei il tuo database Notion per la sincronizzazione stock, devi configurare **esattamente questi campi** con i **nomi esatti**:

## ✅ Campi Obbligatori

### 1. **Name** (Title)
- **Tipo**: Title
- **Descrizione**: Nome del prodotto
- **Obbligatorio**: ✅ Sì
- **Nota**: Viene creato automaticamente come campo principale

**Esempio:**
```
Maglietta Blu
Jeans Nero
Scarpe Rosse
```

---

### 2. **SKU** (Rich Text)
- **Tipo**: Rich Text (o Text)
- **Descrizione**: Codice SKU univoco del prodotto
- **Obbligatorio**: ✅ Sì
- **Importante**: **Deve corrispondere esattamente allo SKU in WooCommerce**

**Esempio:**
```
MAGLIA-001
JEANS-BLACK-42
SCARPE-ROSSO-M
```

> ⚠️ **CRITICALE**: Senza SKU corretto, la sincronizzazione non funzionerà!

---

### 3. **Stock** (Number)
- **Tipo**: Number
- **Descrizione**: Quantità di stock attuale
- **Obbligatorio**: ✅ Sì
- **Range**: Qualsiasi numero (positivo, negativo, zero)

**Esempio:**
```
45
0
150
```

---

## ❌ Campi Opzionali (ma Consigliati)

### 4. **Price** (Number)
- **Tipo**: Number
- **Descrizione**: Prezzo di vendita
- **Obbligatorio**: ❌ No
- **Formato**: Decimale (es. 19.99)

**Perché utile**: 
- L'AI Agent rileva se manca
- Utile per reportistica
- Sincronizzazione prezzo futuro

---

### 5. **Category** (Select)
- **Tipo**: Select
- **Descrizione**: Categoria del prodotto
- **Obbligatorio**: ❌ No
- **Opzioni consigliate**:
  - Abbigliamento
  - Scarpe
  - Accessori
  - Elettronica
  - Altro

**Perché utile**:
- Filtrare prodotti per categoria
- Analisi per gruppo
- Organizzazione database

---

### 6. **Status** (Select)
- **Tipo**: Select
- **Descrizione**: Stato del prodotto
- **Obbligatorio**: ❌ No
- **Opzioni consigliate**:
  - Active (Attivo)
  - Inactive (Inattivo)
  - Draft (Bozza)
  - Discontinued (Discontinuato)

**Perché utile**:
- Controllare quali prodotti sincronizzare
- Identificare prodotti da rimuovere
- AI Agent rileva prodotti esauriti ma attivi

---

### 7. **Last Sync** (Last Edited Time)
- **Tipo**: Last Edited Time
- **Descrizione**: Data/ora ultimo aggiornamento
- **Obbligatorio**: ❌ No (Automatico)
- **Note**: Si aggiorna automaticamente ogni volta che modifica la riga

---

### 8. **Notes** (Rich Text)
- **Tipo**: Rich Text
- **Descrizione**: Note aggiuntive sul prodotto
- **Obbligatorio**: ❌ No
- **Utilità**: 
  - Note sulla sincronizzazione
  - Avvisi AI Agent
  - Memo prodotto

---

## 🛠️ Come Creare il Database in Notion

### Passo 1: Crea un Nuovo Database

1. Apri Notion
2. Vai alla tua workspace
3. Clicca **+ Add a page**
4. Seleziona **Database → Table**
5. Scegli un nome (es. "Stock Management")

---

### Passo 2: Configura i Campi

Il database parte con 3 campi di default:
- `Name` (Title) ✅ **Tieni questo**
- Due campi vuoti ❌ Elimina

#### Aggiungi i Campi:

**Aggiungi campo "SKU":**
1. Clicca **+** (aggiungi campo nuovo)
2. Nome: `SKU`
3. Tipo: `Text` (o Rich Text)
4. Salva

**Aggiungi campo "Stock":**
1. Clicca **+**
2. Nome: `Stock`
3. Tipo: `Number`
4. Salva

**Aggiungi campo "Price":**
1. Clicca **+**
2. Nome: `Price`
3. Tipo: `Number`
4. Salva

**Aggiungi campo "Category":**
1. Clicca **+**
2. Nome: `Category`
3. Tipo: `Select`
4. Opzioni:
   - Abbigliamento
   - Scarpe
   - Accessori
   - Elettronica
   - Altro
5. Salva

**Aggiungi campo "Status":**
1. Clicca **+**
2. Nome: `Status`
3. Tipo: `Select`
4. Opzioni:
   - Active
   - Inactive
   - Draft
   - Discontinued
5. Salva

**Aggiungi campo "Notes":**
1. Clicca **+**
2. Nome: `Notes`
3. Tipo: `Rich Text`
4. Salva

---

### Passo 3: Verifica Struttura

Il tuo database dovrebbe avere questi campi:

| Campo | Tipo | Obbligatorio | Status |
|-------|------|-----------|--------|
| **Name** | Title | ✅ | ✓ Setup |
| **SKU** | Text | ✅ | ✓ Setup |
| **Stock** | Number | ✅ | ✓ Setup |
| **Price** | Number | ❌ | ✓ Setup |
| **Category** | Select | ❌ | ✓ Setup |
| **Status** | Select | ❌ | ✓ Setup |
| **Notes** | Rich Text | ❌ | ✓ Setup |

---

## 📝 Popola il Database

### Manuale (Piccolo Volume)
1. Apri il database Notion
2. Clicca **+ Add a new page** o **+ New**
3. Compila i campi:
   ```
   Name: Maglietta Blu
   SKU: MAGLIA-001          ← Deve corrispondere a WooCommerce!
   Stock: 45
   Price: 19.99
   Category: Abbigliamento
   Status: Active
   Notes: Sincronizzato con WooCommerce
   ```
4. Ripeti per ogni prodotto

### Automatico (Grandi Volumi)
Usa import CSV o API Notion:

**Formato CSV:**
```
Name,SKU,Stock,Price,Category,Status
Maglietta Blu,MAGLIA-001,45,19.99,Abbigliamento,Active
Jeans Nero,JEANS-001,30,49.99,Abbigliamento,Active
Scarpe Rosse,SCARPE-001,15,79.99,Scarpe,Active
```

**Come importare:**
1. Clicca i tre puntini **...**
2. Seleziona **Import**
3. Scegli CSV
4. Seleziona il file
5. Mappa i campi
6. Importa

---

## 🔑 Ottenere Database ID

Il sistema ha bisogno del **NOTION_DATABASE_ID** nel file `.env`

### Come trovarlo:

1. **Apri il tuo database Notion nel browser**
2. Guarda l'URL:
   ```
   https://www.notion.so/tuousername/xxxxxxxxxxxxxxxxxxxxx?v=yyyyyyyyyyyyyyyy
   ```
3. La parte `xxxxxxxxxxxxxxxxxxxxx` è il **DATABASE_ID**
4. Copia e incolla nel `.env`:
   ```env
   NOTION_DATABASE_ID=xxxxxxxxxxxxxxxxxxxxx
   ```

**Nota**: L'ID non contiene trattini, è una stringa alfanumerica lunga

---

## ✨ Esempio Database Completo

```
Database: Stock Management

Row 1:
├─ Name: Maglietta Blu
├─ SKU: MAGLIA-001
├─ Stock: 45
├─ Price: 19.99
├─ Category: Abbigliamento
├─ Status: Active
└─ Notes: In stock, sincronizzato

Row 2:
├─ Name: Jeans Nero
├─ SKU: JEANS-001
├─ Stock: 0
├─ Price: 49.99
├─ Category: Abbigliamento
├─ Status: Inactive
└─ Notes: Esaurito, riordine in corso

Row 3:
├─ Name: Scarpe Rosse
├─ SKU: SCARPE-001
├─ Stock: 3
├─ Price: 79.99
├─ Category: Scarpe
├─ Status: Active
└─ Notes: Stock critico! Riordinare urgente
```

---

## 🤖 Come Funziona con l'AI Agent

L'AI Agent analizza questi campi:

### Input
- `SKU` - Per collegare a WooCommerce
- `Stock` - Per confrontare e suggerire
- `Price` - Per rilevare se mancante
- `Status` - Per verificare coerenza

### Output nel campo Notes
L'AI Agent potrebbe aggiungere:
```
🔄 [Sincronizzazione 26/01/2026 10:30]
⚠️  Stock critico (3 unità)
💡 Riordinare 75 unità (URGENT)
```

---

## ⚠️ Errori Comuni

### ❌ SKU non corrisponde WooCommerce
**Problema**: Stock non sincronizza
**Soluzione**: Verifica che SKU sia **identico** in entrambi i sistemi (case-sensitive)

### ❌ Nome campo errato (es. "stock" invece di "Stock")
**Problema**: Sync fallisce silenziosamente
**Soluzione**: Controlla che nomi siano **esattamente** come in tabella

### ❌ Tipo campo sbagliato (es. Text invece di Number per Stock)
**Problema**: Errore di parsing
**Soluzione**: Usa **Number** per Stock, **Text** per SKU

### ❌ Dimenticato di condividere DB con integrazione Notion
**Problema**: "Permission denied" error
**Soluzione**: Clicca Share → Condividi con integrazione creata

---

## 🔐 Sicurezza

### Informazioni Sensibili
Non mettere nel database Notion:
- ❌ Password
- ❌ Costi fornitori (non necessario)
- ❌ Dati personali clienti

### Condivisione
- ✅ Condividi database solo con integrazione AI
- ✅ Usa role "Editor" per integrazione
- ✅ Non condividere link pubblico

---

## 📞 Supporto

Se hai problemi:

1. **Verifica Setup Database**
   - Controlla nomi campi (case-sensitive!)
   - Verifica tipi campo

2. **Verifica Integrazione**
   - Assicurati token Notion sia valido
   - Verifica database sia condiviso

3. **Vedi Logs**
   ```bash
   docker-compose logs -f stock-sync
   ```

4. **Testa Connessione**
   ```bash
   python test_ai_agent.py
   ```

---

## 🎉 Pronto!

Una volta configurato il database Notion con tutti i campi, sei pronto a:

1. Configurare il `.env` con credenziali
2. Avviare il sistema: `docker-compose up -d`
3. Monitorare sincronizzazione: `docker-compose logs -f`
4. Beneficiare dell'AI Agent che analizza lo stock! 🤖

Buona sincronizzazione! 📦

````
