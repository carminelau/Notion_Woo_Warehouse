````markdown
# 🤖 AI Agent - Documentazione Completa

## Panoramica

L'AI Agent è un sistema intelligente integrato nel Stock Management che analizza automaticamente i dati di stock e fornisce insights, avvisi e suggerimenti basati su analisi avanzata.

## Componenti Principali

### 1. AIAgent (`sync/ai_agent.py`)

Classe principale che gestisce tutte le analisi intelligenti.

#### Metodi Disponibili

##### `analyze_stock_discrepancies(woo_products, notion_items)`
Analizza le differenze di stock tra i due sistemi.

**Parametri:**
- `woo_products`: Lista prodotti WooCommerce
- `notion_items`: Lista item Notion

**Ritorna:**
```python
{
    "total_products": int,
    "total_items": int,
    "discrepancies": [
        {
            "sku": str,
            "product_name": str,
            "stock_woo": int,
            "stock_notion": int,
            "difference": int,
            "severity": "LOW|MEDIUM|HIGH|CRITICAL"
        }
    ],
    "warnings": [str],
    "insights": [str]
}
```

**Esempio:**
```python
analysis = ai_agent.analyze_stock_discrepancies(woo_products, notion_items)
if analysis['discrepancies']:
    for disc in analysis['discrepancies']:
        print(f"SKU: {disc['sku']}, Severity: {disc['severity']}")
```

---

##### `detect_anomalies(products)`
Rileva anomalie nei dati dei prodotti.

**Tipi di Anomalie Rilevate:**

| Tipo | Severity | Descrizione |
|------|----------|-------------|
| `NEGATIVE_STOCK` | CRITICAL | Stock negativo rilevato |
| `OUT_OF_STOCK` | HIGH | Prodotto esaurito ma ancora attivo |
| `MISSING_PRICE` | MEDIUM | Prezzo non impostato |
| `UNUSUAL_STOCK` | MEDIUM | Stock insolitamente alto (>10000) |

**Ritorna:**
```python
[
    {
        "type": str,
        "severity": "CRITICAL|HIGH|MEDIUM",
        "product_id": int,
        "product_name": str,
        "message": str,
        "recommendation": str
    }
]
```

**Esempio:**
```python
anomalies = ai_agent.detect_anomalies(woo_products)
for anomaly in anomalies:
    if anomaly['severity'] == 'CRITICAL':
        print(f"🚨 {anomaly['message']}")
        print(f"💡 {anomaly['recommendation']}")
```

---

##### `generate_reorder_suggestions(products, threshold=10)`
Genera suggerimenti intelligenti di riordino.

**Parametri:**
- `products`: Lista prodotti da analizzare
- `threshold`: Soglia di stock (default: 10 unità)

**Ritorna:**
```python
[
    {
        "product_id": int,
        "product_name": str,
        "current_stock": int,
        "threshold": int,
        "urgency": "CRITICAL|HIGH|MEDIUM",
        "recommended_order": int,
        "message": str
    }
]
```

**Logica di Urgenza:**
- **CRITICAL**: Stock ≤ 25% della soglia
- **HIGH**: Stock ≤ 50% della soglia
- **MEDIUM**: Stock tra 50% e 100% della soglia

**Esempio:**
```python
suggestions = ai_agent.generate_reorder_suggestions(woo_products, threshold=10)
for sugg in suggestions:
    if sugg['urgency'] == 'CRITICAL':
        print(f"🔴 URGENTE: {sugg['product_name']}")
        print(f"Ordina: {sugg['recommended_order']} unità")
```

---

##### `generate_intelligent_notes(product, context)`
Genera note intelligenti basate su analisi.

**Parametri:**
- `product`: Dati del prodotto
- `context`: Contesto con anomalie e suggerimenti

**Ritorna:** String con note formattate

**Esempio:**
```python
context = {
    'anomalies': anomalies,
    'suggestions': suggestions
}
notes = ai_agent.generate_intelligent_notes(product, context)
print(notes)  # Output: "🔄 [Sincronizzazione 26/01/2026 10:30] | ⏰ Stock critico (5 unità) | 💡 Stock basso..."
```

---

### 2. NotionNotifier (`sync/notifier.py`)

Gestisce le notifiche e i report di sincronizzazione.

#### Metodi Disponibili

##### `notify_discrepancies(discrepancies)`
Notifica le discrepanze trovate nei log.

##### `notify_anomalies(anomalies)`
Notifica le anomalie rilevate con level di logging appropriato.

##### `notify_reorder_suggestions(suggestions)`
Notifica i suggerimenti di riordino.

##### `create_sync_report(sync_data)`
Crea un report completo di sincronizzazione.

**Ritorna:** String formattato con report

**Esempio Output:**
```
📊 REPORT SINCRONIZZAZIONE
========================================
⏰ Data/Ora: 26/01/2026 10:30:45

📦 Prodotti WooCommerce: 150
📋 Item Notion: 145
⚠️  Discrepanze: 3
💡 Insights:
  • 📊 Stock medio WooCommerce: 45 unità
  • 📦 5 prodotti esauriti
  • 🔄 Tasso di sincronizzazione: 96.7%

🔍 Anomalie rilevate: 2
  • [HIGH] Maglietta Blu - Stock negativo: -5
  • [MEDIUM] Jeans Nero - Prezzo non impostato

💡 Suggerimenti riordino: 4
  • Scarpe Rosse (3 unità)
  • Cappello Verde (7 unità)
```

---

## Flusso di Esecuzione

Durante ogni ciclo di sincronizzazione:

```
1. Sincronizzazione Stock (Bidirezionale)
   ↓
2. Recupera dati da WooCommerce e Notion
   ↓
3. Analisi Discrepanze
   ├─ Identifica SKU non sincronizzati
   ├─ Calcola differenze di stock
   └─ Determina severity
   ↓
4. Rilevamento Anomalie
   ├─ Stock negativo
   ├─ Prodotti esauriti
   ├─ Prezzi mancanti
   └─ Valori inusuali
   ↓
5. Suggerimenti Riordino
   ├─ Identifica prodotti sotto soglia
   ├─ Calcola urgenza
   └─ Suggerisce quantità
   ↓
6. Notifiche
   ├─ Log avvisi/errori
   ├─ Alert su anomalie critiche
   └─ Summary report
   ↓
7. Fine ciclo - Attesa prossima sincronizzazione
```

---

## Configurazione

### Variabili di Ambiente

```env
# AI Agent settings
AI_MODEL=local                          # Modello AI (attualmente solo "local")
STOCK_WARNING_THRESHOLD=10              # Soglia unità per avvisi
```

### Nel Codice

Per customizzare i parametri di analisi:

```python
from sync.ai_agent import AIAgent

ai_agent = AIAgent()

# Personalizzare la soglia di riordino
suggestions = ai_agent.generate_reorder_suggestions(
    products=woo_products,
    threshold=20  # Anzichè 10
)
```

---

## Esempi di Utilizzo

### Esempio 1: Analisi Completa

```python
from sync.ai_agent import AIAgent
from sync.notifier import NotionNotifier

ai_agent = AIAgent()
notifier = NotionNotifier(notion_client)

# Recupera dati
woo_products = woo_client.get_products()
notion_items = notion_client.get_all_items()

# Analisi
analysis = ai_agent.analyze_stock_discrepancies(woo_products, notion_items)
anomalies = ai_agent.detect_anomalies(woo_products)
suggestions = ai_agent.generate_reorder_suggestions(woo_products)

# Notifiche
notifier.notify_discrepancies(analysis['discrepancies'])
notifier.notify_anomalies(anomalies)
notifier.notify_reorder_suggestions(suggestions)

# Report
report = notifier.create_sync_report({
    'analysis': analysis,
    'anomalies': anomalies,
    'suggestions': suggestions
})
print(report)
```

### Esempio 2: Filtrare Anomalie Critiche

```python
# Ottieni solo anomalie critiche
critical_anomalies = [
    a for a in anomalies 
    if a['severity'] == 'CRITICAL'
]

if critical_anomalies:
    print("🚨 ANOMALIE CRITICHE RILEVATE!")
    for anomaly in critical_anomalies:
        print(f"  {anomaly['product_name']}: {anomaly['message']}")
```

### Esempio 3: Suggerimenti Urgenti

```python
# Ottieni suggerimenti urgenti di riordino
urgent = [
    s for s in suggestions 
    if s['urgency'] in ['CRITICAL', 'HIGH']
]

print(f"📌 {len(urgent)} riordini urgenti necessari:")
for sugg in urgent:
    print(f"  {sugg['product_name']}: ordina {sugg['recommended_order']} unità")
```

---

## Limiti Attuali e Possibili Estensioni

### Limiti Attuali:
- Analisi basata su regole (non ML)
- Nessuna integrazione API esterna
- Memoria a breve termine (nessuna persistenza di dati storici)

### Possibili Estensioni Future:
- ✨ Integrazione con modelli LLM (OpenAI, Claude, Gemini)
- 📈 Machine Learning per previsione di vendite
- 📊 Persistenza dati storici per analisi trend
- 🔔 Notifiche push via email/Slack
- 🎯 Machine Learning per categorizazione automatica
- 📱 Dashboard web per visualizzazione

---

## Troubleshooting

### Nessuna anomalia rilevata
- Verifica che i dati siano corretti
- Aumenta il LOG_LEVEL a DEBUG per dettagli
- Controlla che i campi richiesti esistano in Notion

### Suggerimenti di riordino non vengono generati
- Verifica che STOCK_WARNING_THRESHOLD sia configurato
- Controlla che i prodotti abbiano stock_quantity
- Aumenta il log level per debug

### Report non viene generato
- Verifica che l'analisi sia completa
- Controlla il formato dei dati in input

---

## Performance

L'AI Agent è ottimizzato per performance:
- **Tempo di analisi**: ~100-200ms per 1000 prodotti
- **Memoria**: ~10-20MB per set di dati standard
- **CPU**: Minimo (100% Python puro, no ML pesante)

---

## Sicurezza

- ✅ Nessun dato sensibile salvato
- ✅ Nessuna comunicazione con servizi esterni
- ✅ Solo analisi locale
- ✅ Conforme GDPR (nessun tracciamento)

---

Per domande o suggerimenti, consulta i log dettagliati con:
```bash
docker-compose logs -f stock-sync
```

````
