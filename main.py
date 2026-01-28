import os
import logging
from dotenv import load_dotenv
from loguru import logger
import schedule
import time
from sync.woocommerce_client import WooCommerceClient
from sync.notion_client import NotionClient
from sync.stock_sync import StockSynchronizer
from sync.ai_agent import AIAgent
from sync.notifier import NotionNotifier

# Carica variabili di ambiente
load_dotenv()

# Configura logging
log_level = os.getenv('LOG_LEVEL', 'INFO')
logger.remove()
logger.add(
    "logs/stock_sync.log",
    level=log_level,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    rotation="500 MB",
    retention="7 days"
)
logger.add(lambda msg: print(msg, end=""), level=log_level)

# Inizializza client
def initialize_clients():
    """Inizializza i client per WooCommerce e Notion"""
    try:
        woo_client = WooCommerceClient(
            api_url=os.getenv('WOOCOMMERCE_API_URL'),
            consumer_key=os.getenv('WOOCOMMERCE_CONSUMER_KEY'),
            consumer_secret=os.getenv('WOOCOMMERCE_CONSUMER_SECRET')
        )
        
        notion_client = NotionClient(
            token=os.getenv('NOTION_TOKEN'),
            database_id=os.getenv('NOTION_DATABASE_ID')
        )
        
        # Inizializza AI Agent e Notifier
        ai_agent = AIAgent()
        notifier = NotionNotifier(notion_client)
        
        logger.info("✓ Client inizializzati con successo")
        return woo_client, notion_client, ai_agent, notifier
    except Exception as e:
        logger.error(f"✗ Errore nell'inizializzazione dei client: {e}")
        raise

def sync_job(woo_client, notion_client, synchronizer, ai_agent, notifier):
    """Esegue il job di sincronizzazione con analisi AI"""
    try:
        logger.info("🔄 Inizio sincronizzazione stock...")
        
        # Sincronizzazione standard
        synchronizer.sync()
        
        # ===== ANALISI AI =====
        logger.info("🤖 Avvio analisi AI...")
        
        # Recupera dati per analisi
        woo_products = woo_client.get_products()
        notion_items = notion_client.get_all_items()
        
        # Analisi discrepanze
        analysis_result = ai_agent.analyze_stock_discrepancies(woo_products, notion_items)
        notifier.notify_discrepancies(analysis_result.get('discrepancies', []))
        
        # Rilevamento anomalie
        anomalies = ai_agent.detect_anomalies(woo_products)
        notifier.notify_anomalies(anomalies)
        
        # Suggerimenti di riordino
        suggestions = ai_agent.generate_reorder_suggestions(woo_products)
        notifier.notify_reorder_suggestions(suggestions)
        
        # Genera report
        sync_report = notifier.create_sync_report({
            'analysis': analysis_result,
            'anomalies': anomalies,
            'suggestions': suggestions
        })
        logger.info(f"\n{sync_report}")
        
        logger.info("✓ Sincronizzazione e analisi AI completate con successo")
        
    except Exception as e:
        logger.error(f"✗ Errore durante la sincronizzazione: {e}", exc_info=True)

def main():
    """Funzione principale"""
    logger.info("=" * 50)
    logger.info("🚀 Stock Management Sync - Avvio")
    logger.info("🤖 AI Agent abilitato")
    logger.info("=" * 50)
    
    try:
        # Inizializza client
        woo_client, notion_client, ai_agent, notifier = initialize_clients()
        synchronizer = StockSynchronizer(woo_client, notion_client)
        
        # Esegui sincronizzazione iniziale
        sync_job(woo_client, notion_client, synchronizer, ai_agent, notifier)
        
        # Configura sync periodico
        sync_interval = int(os.getenv('SYNC_INTERVAL', 300))
        logger.info(f"⏱️  Intervallo di sincronizzazione: {sync_interval} secondi")
        
        schedule.every(sync_interval).seconds.do(
            sync_job, 
            woo_client=woo_client, 
            notion_client=notion_client,
            synchronizer=synchronizer,
            ai_agent=ai_agent,
            notifier=notifier
        )
        
        logger.info("✓ Scheduler avviato. In attesa di eseguire i job...")
        
        # Loop infinito per eseguire i job schedulati
        while True:
            schedule.run_pending()
            time.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("⛔ Sincronizzazione interrotta dall'utente")
    except Exception as e:
        logger.error(f"✗ Errore critico: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
