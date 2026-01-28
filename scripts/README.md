## 🔧 Scripts - Utility e Template

Questa cartella contiene script di **test, debug e utility** per lo sviluppo.

### 📋 File Disponibili

#### `add_sku_template.py`
Template generico per aggiungere SKU automatici ai prodotti WooCommerce.

**Uso:**
```bash
# Mostra i primi 100 prodotti e aggiunge SKU con prefisso PROD
python scripts/add_sku_template.py

# Sovrascrive anche SKU esistenti
python scripts/add_sku_template.py --overwrite

# Cambia prefisso SKU
python scripts/add_sku_template.py --prefix=CUSTOM

# Elabora solo i primi 10 prodotti
python scripts/add_sku_template.py --limit=10

# Combina opzioni
python scripts/add_sku_template.py --prefix=SHOP --overwrite --limit=50
```

**Come personalizzare:**
1. Copia il file: `cp add_sku_template.py add_custom_skus.py`
2. Modifica la funzione `generate_sku()` con il tuo formato SKU
3. Adatta la logica alle tue esigenze

---

#### `debug_product_template.py`
Tool per ispezionare la struttura dei tuoi prodotti WooCommerce.

**Uso:**
```bash
# Ispeziona i primi 5 prodotti
python scripts/debug_product_template.py

# Ispeziona i primi 10 prodotti
python scripts/debug_product_template.py --limit=10

# Cerca un prodotto per SKU
python scripts/debug_product_template.py --sku=ABC-123

# Cerca un prodotto per ID
python scripts/debug_product_template.py --id=42

# Combina
python scripts/debug_product_template.py --limit=20
```

**Output:**
- Stampa informazioni su console
- Genera file JSON (`debug_product_*.json`) per analisi dettagliata
- Mostra attributi, metadati e varianti

---

### 🚀 Come Usare gli Script

#### Setup Iniziale
```bash
# 1. Assicurati di avere .env configurato con credenziali WooCommerce
cat .env.example  # Verifica i campi richiesti

# 2. Installa dipendenze
pip install -r requirements.txt
```

#### Workflow Tipico

**1. Analizzare i dati:**
```bash
python scripts/debug_product_template.py --limit=5
```

**2. Verificare il formato personalizzato:**
Modifica `add_sku_template.py` e testa con `--limit=1`

**3. Eseguire in produzione:**
```bash
python scripts/add_sku_template.py --prefix=SHOP --limit=100
```

---

### 📝 Creare i Tuoi Script

Usa questi template come base per i tuoi script custom:

**Passo 1:** Copia il template
```bash
cp add_sku_template.py add_my_custom_script.py
```

**Passo 2:** Modifica secondo le tue esigenze
```python
def generate_sku(product_id, variant_id=None, prefix="PROD"):
    # TODO: Personalizza qui!
    # Esempio: combina categoria + ID
    # return f"{categoria}-{product_id}"
    pass
```

**Passo 3:** Testa in sicurezza
```bash
# Test con pochi prodotti
python scripts/add_my_custom_script.py --limit=1

# Se tutto ok, esegui con limite ragionevole
python scripts/add_my_custom_script.py --limit=100

# Infine, esegui su tutti
python scripts/add_my_custom_script.py
```

---

### ⚠️ Best Practices

1. **Sempre testare con `--limit=1` prima** di eseguire su tutti i prodotti
2. **Fai un backup** dei tuoi dati prima di modifiche importanti
3. **Usa `--overwrite` con cautela** - potrebbe perdere dati!
4. **Verifica il log** dopo l'esecuzione
5. **Salva i file JSON generati** per analisi future

---

### 🔒 Sicurezza

- ✅ Non committare script con logica specifica sensibile
- ✅ Non committare `.env` con credenziali reali
- ✅ Usa variabili d'ambiente per configurazione
- ✅ Verifica sempre cosa fanno gli script prima di eseguirli

---

### 🐛 Debug

Se uno script ha problemi:

```bash
# Abilita debug
DEBUG=1 python scripts/add_sku_template.py --limit=1

# Controlla i file JSON generati
cat debug_product_*.json

# Vedi i log di sincronizzazione
tail -f ../logs/stock_sync.log
```

---

### 📞 Supporto

Se hai domande su come usare o modificare gli script:
1. Leggi i commenti nel codice
2. Controlla la documentazione in `docs/`
3. Testa con `--limit=1` per debugging
4. Usa i file JSON generati per capire la struttura dati

---

**Nota:** Questi script sono per **development e testing**. 
Per operazioni in produzione, considera di automatizzarle tramite `main.py` con scheduling appropriato.
