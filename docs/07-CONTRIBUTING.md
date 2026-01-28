````markdown
# 👥 Guida per Contribuire

Grazie per l'interesse nel contribuire a Stock Management Docker! Questa guida ti aiuterà a iniziare.

## 🚀 Per Iniziare

### 1. Fork il Repository
1. Vai su GitHub
2. Clicca **Fork** per creare una copia sotto il tuo account

### 2. Clone il Repository Locale
```bash
git clone https://github.com/TUO_USERNAME/Docker_Stock_management.git
cd Docker_Stock_management
```

### 3. Crea un Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Su Linux/Mac
# oppure
.\venv\Scripts\activate   # Su Windows
```

### 4. Installa le Dipendenze
```bash
pip install -r requirements.txt
```

### 5. Configura .env per Development
```bash
cp .env.example .env
# Modifica .env con le tue credenziali di test
```

## 📋 Git Workflow

### Branch Naming

Usa nomi descrittivi per i branch:

```
feature/nome-feature          # Nuove funzionalità
bugfix/descrizione-bug        # Correzione bug
docs/descrizione-docs         # Miglioramenti documentazione
refactor/descrizione-refactor # Refactoring codice
test/descrizione-test         # Aggiunte test
```

**Esempi:**
```
feature/ai-email-notifications
bugfix/sync-timeout-issue
docs/setup-guide-update
refactor/client-abstraction
test/ai-agent-coverage
```

### Processo di Contribuzione

1. **Crea un branch feature**
   ```bash
   git checkout -b feature/tuo-feature-name
   ```

2. **Fai i tuoi cambiamenti**
   - Modifica i file necessari
   - Segui gli standard di codice (vedi sotto)

3. **Scrivi/Aggiorna i test**
   ```bash
   python test_ai_agent.py  # Se modifichi AI
   ```

4. **Commit i tuoi cambiamenti**
   ```bash
   git add .
   git commit -m "Descrizione chiara del cambio"
   ```
   
   **Formato commit message:**
   ```
   <tipo>(<scope>): <descrizione breve>
   
   <descrizione dettagliata (opzionale)>
   
   Closes #numero-issue (se applicabile)
   ```
   
   **Esempi:**
   ```
   feat(ai): add email notification support
   
   - Integrates email sender for anomaly alerts
   - Configurable via EMAIL_ENABLED env var
   - Defaults to INFO level notifications
   
   Closes #42
   ```

5. **Push il branch**
   ```bash
   git push origin feature/tuo-feature-name
   ```

6. **Crea una Pull Request**
   - Vai su GitHub
   - Clicca **Compare & pull request**
   - Descrivi i cambiamenti nel dettaglio
   - Fai riferimento a issue correlate

## 📋 Pull Request Guidelines

### Descrizione PR

Usa questo template:

```markdown
## Descrizione
Descrivi brevemente cosa fa questo PR.

## Motivazione
Perché è necessario questo cambio?
- Quale problema risolve?
- Quale feature aggiunge?

## Tipo di Cambio
- [ ] Bug fix
- [ ] Nuova feature
- [ ] Breaking change
- [ ] Miglioramento documentazione

## Come Testare?
Passi per testare il cambio:
1. ...
2. ...
3. ...

## Checklist
- [ ] Ho letto le CONTRIBUTING guidelines
- [ ] Ho aggiunto/aggiornato test se necessario
- [ ] Ho aggiornato la documentazione
- [ ] Non ho errori di linting
- [ ] Ho testato localmente

## Breaking Changes
Se ci sono breaking changes, descrivi:
- Quali sono
- Come migrarsi da vecchio a nuovo
```

## 💻 Standard di Codice

### Python Style

Segui **PEP 8**:

```python
# ✅ Buono
def analyze_stock_discrepancies(products, items):
    """Analyze stock differences between systems.
    
    Args:
        products: List of WooCommerce products
        items: List of Notion items
        
    Returns:
        dict: Analysis results with discrepancies
    """
    discrepancies = []
    for product in products:
        # Process product...
        pass
    return {"discrepancies": discrepancies}


# ❌ Cattivo
def analyze_stock_discrepancies(products,items):
    #analyze stock
    disc=[]
    for p in products:
        #process
        pass
    return {'disc': disc}
```

### Naming Conventions

```python
# Costanti
STOCK_WARNING_THRESHOLD = 10
API_TIMEOUT_SECONDS = 30

# Variabili
customer_name = "John"
product_count = 100

# Funzioni
def calculate_total_price():
    pass

# Classi
class WooCommerceClient:
    pass

# Metodi privati
def _calculate_severity(difference):
    pass
```

### Docstring

```python
def generate_reorder_suggestions(products, threshold=10):
    """Generate intelligent reorder suggestions.
    
    This method analyzes product stock levels and generates
    reorder suggestions based on the configured threshold.
    
    Args:
        products (list): List of product dictionaries
        threshold (int, optional): Stock warning threshold. Defaults to 10.
    
    Returns:
        list: List of suggestion dictionaries with keys:
            - product_id (int): Product ID
            - product_name (str): Product name
            - current_stock (int): Current stock level
            - urgency (str): One of CRITICAL, HIGH, MEDIUM
            - recommended_order (int): Suggested order quantity
            - message (str): Human-readable message
    
    Raises:
        ValueError: If products is empty or threshold < 0
        
    Example:
        >>> suggestions = ai_agent.generate_reorder_suggestions(products)
        >>> for sugg in suggestions:
        ...     print(f"Order {sugg['recommended_order']} units")
    """
    pass
```

### Logging

```python
from loguru import logger

# ✅ Buono
logger.info(f"Processing {len(products)} products")
logger.warning(f"Stock discrepancy for {sku}: {diff} units")
logger.error(f"API error: {error_message}", exc_info=True)

# ❌ Cattivo
print("Processing products")
print("ERROR: something went wrong")
```

### Comments

```python
# ✅ Buono - Spiega il perché, non il cosa
# Stock ≤ 25% della soglia è considerato critico
if stock <= threshold * 0.25:
    urgency = "CRITICAL"

# ❌ Cattivo
# Incrementa i (non serve, è ovvio)
i += 1

# ❌ Cattivo - Codice commentato
# client.update_product()
# notifier.send_email()
```

## 🧪 Testing

### Eseguire i Test

```bash
# Test AI Agent
python test_ai_agent.py

# Test specifico (se usi pytest)
pytest tests/test_ai_agent.py
```

### Scrivere i Test

```python
def test_analyze_stock_discrepancies():
    """Test analyze_stock_discrepancies with sample data."""
    # Arrange
    ai_agent = AIAgent()
    products = [
        {"id": 1, "sku": "TEST-001", "stock": 50},
        {"id": 2, "sku": "TEST-002", "stock": 0}
    ]
    items = [
        {"sku": "TEST-001", "stock": 40},
        {"sku": "TEST-003", "stock": 100}
    ]
    
    # Act
    result = ai_agent.analyze_stock_discrepancies(products, items)
    
    # Assert
    assert len(result["discrepancies"]) == 2
    assert result["discrepancies"][0]["severity"] in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
```

## 📚 Documentazione

### Updating Docs

Se modifichi o aggiungi funzionalità, aggiorna la documentazione:

1. **Aggiorna il docstring** nel codice
2. **Aggiorna il README** se è una feature pubblica
3. **Aggiorna la documentazione** nella cartella `docs/`
4. **Aggiorna il CHANGELOG** in `docs/05-CHANGELOG.md`

### Documentazione Style

```markdown
# Usa intestazioni gerarchiche
## Sezioni principali
### Sottosezioni
#### Dettagli

**Grassetto** per enfasi importante
`Codice inline` per riferimenti codice

# Codice
\`\`\`python
# Codice di esempio
\`\`\`

# Liste
- Punto 1
- Punto 2
  - Sottopunto
```

## 🔒 Sicurezza

### NO Credenziali
- ❌ Mai committare `.env` con credenziali reali
- ❌ Mai committare token API
- ❌ Mai committare password

### NO Dati Sensibili
- ❌ Mai loggare credenziali
- ❌ Mai printare token
- ❌ Mai salvare dati personali

### SI Sicurezza
- ✅ Usa `.env.example` come template
- ✅ Valida tutti gli input
- ✅ Usa variabili di ambiente per secrets
- ✅ Sanitizza i log

## 🐛 Segnalare Bug

### Template Issue

```markdown
## Descrizione Bug
Descrizione chiara del bug.

## Passi per Riprodurre
1. ...
2. ...
3. ...

## Comportamento Atteso
Cosa dovrebbe accadere?

## Comportamento Effettivo
Cosa accade invece?

## Ambiente
- OS: Windows 10
- Python: 3.11
- Docker: Desktop
- Branch: main

## Log/Errore
```
Copia dell'errore o log
```

## Possibile Soluzione
(opzionale) Come pensi possa essere risolto?
```

## 💡 Proposte Feature

### Template Feature Request

```markdown
## Descrizione
Descrizione breve della feature.

## Motivazione
Perché è utile?

## Soluzione Proposta
Come implementarla?

## Alternativas
Altre soluzioni possibili?

## Contesto Aggiuntivo
Altro che pensi sia rilevante?
```

## 📞 Comunicazione

### Codice di Condotta
- Sii rispettoso
- Sii costruttivo
- Sii inclusivo
- Sii paziente

### Chiedere Aiuto
1. Consulta la documentazione in `docs/`
2. Cerca issue simili su GitHub
3. Apri una discussion per domande generali
4. Apri un issue solo se hai trovato un bug

## 🎯 Area di Contribuzione

### Areas Accettati Volontariamente

```
CORE
├── Bug fixes                          ✅ Benvenuto
├── Performance improvements           ✅ Benvenuto
├── Refactoring (mantenere API)       ✅ Benvenuto
└── Breaking changes                   ⚠️ Discussione prima

FEATURES
├── Miglioramenti AI                   ✅ Benvenuto
├── Nuovi notifier (Slack, Email)      ✅ Benvenuto
├── Dashboard web                      ✅ Benvenuto
├── ML integration                     ✅ Benvenuto
└── LLM integration                    ✅ Benvenuto

DOCS
├── Correzioni typo                    ✅ Benvenuto
├── Miglioramenti guide                ✅ Benvenuto
├── Traduzioni nuove lingue            ✅ Benvenuto
├── Video tutorial                     ✅ Benvenuto
└── Esempi aggiuntivi                  ✅ Benvenuto

TEST
├── Unit test                          ✅ Benvenuto
├── Integration test                   ✅ Benvenuto
├── Performance test                   ✅ Benvenuto
└── Load test                          ✅ Benvenuto
```

## 📜 License

Contribuendo a questo progetto accetti che il tuo codice sia distribuito sotto la stessa licenza del progetto.

## ✨ Grazie!

Apprezziamo ogni contributo! Che sia codice, documentazione, test o semplici segnalazioni di bug, tutto aiuta a migliorare il progetto.

Se hai domande, sentiti libero di aprire una discussion o un issue.

**Felice Contribuzione!** 🚀

````
