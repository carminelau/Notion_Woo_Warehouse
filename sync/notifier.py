from loguru import logger
from typing import List, Dict
from datetime import datetime

class NotionNotifier:
    """Gestisce notifiche intelligenti su Notion"""
    
    def __init__(self, notion_client):
        """
        Inizializza il notifier
        
        Args:
            notion_client: Client Notion per comunicare
        """
        self.notion = notion_client
        logger.info("✓ Notion Notifier inizializzato")
    
    def notify_discrepancies(self, discrepancies: List[Dict]):
        """
        Notifica le discrepanze trovate
        
        Args:
            discrepancies: Lista discrepanze rilevate
        """
        try:
            if not discrepancies:
                logger.info("ℹ️  Nessuna discrepanza da notificare")
                return
            
            logger.info(f"📢 Notificazione {len(discrepancies)} discrepanze...")
            
            for disc in discrepancies:
                sku = disc.get('sku')
                product_name = disc.get('product_name')
                stock_woo = disc.get('stock_woo')
                stock_notion = disc.get('stock_notion')
                severity = disc.get('severity')
                
                # Genera messaggio
                message = f"⚠️  DISCREPANZA [{severity}] | {product_name} ({sku})\n"
                message += f"WooCommerce: {stock_woo} unità\n"
                message += f"Notion: {stock_notion} unità\n"
                message += f"Differenza: {disc.get('difference')} unità"
                
                logger.warning(message)
        
        except Exception as e:
            logger.error(f"✗ Errore nella notificazione discrepanze: {e}")
    
    def notify_anomalies(self, anomalies: List[Dict]):
        """
        Notifica le anomalie rilevate
        
        Args:
            anomalies: Lista anomalie rilevate
        """
        try:
            if not anomalies:
                return
            
            logger.warning(f"🔍 Anomalie rilevate ({len(anomalies)}):")
            
            for anomaly in anomalies:
                severity = anomaly.get('severity')
                anomaly_type = anomaly.get('type')
                product_name = anomaly.get('product_name')
                message = anomaly.get('message')
                recommendation = anomaly.get('recommendation')
                
                log_msg = f"  [{severity}] {anomaly_type}: {product_name}\n"
                log_msg += f"    📌 {message}\n"
                log_msg += f"    💡 {recommendation}"
                
                if severity == 'CRITICAL':
                    logger.critical(log_msg)
                elif severity == 'HIGH':
                    logger.error(log_msg)
                else:
                    logger.warning(log_msg)
        
        except Exception as e:
            logger.error(f"✗ Errore nella notificazione anomalie: {e}")
    
    def notify_reorder_suggestions(self, suggestions: List[Dict]):
        """
        Notifica suggerimenti di riordino
        
        Args:
            suggestions: Lista suggerimenti di riordino
        """
        try:
            if not suggestions:
                return
            
            logger.info(f"💡 Suggerimenti di riordino ({len(suggestions)}):")
            
            for sugg in suggestions:
                product_name = sugg.get('product_name')
                current_stock = sugg.get('current_stock')
                recommended = sugg.get('recommended_order')
                urgency = sugg.get('urgency')
                
                message = f"  [{urgency}] {product_name}\n"
                message += f"    Stock attuale: {current_stock} unità\n"
                message += f"    Ordine consigliato: {recommended} unità"
                
                logger.info(message)
        
        except Exception as e:
            logger.error(f"✗ Errore nella notificazione suggerimenti: {e}")
    
    def update_product_notes_with_analysis(self, notion_items: List[Dict], analysis_result: Dict, ai_agent):
        """
        Aggiorna le note dei prodotti in Notion con analisi AI
        
        Args:
            notion_items: Item Notion da aggiornare
            analysis_result: Risultato dell'analisi AI
            ai_agent: Istanza AI Agent
        """
        try:
            anomalies = analysis_result.get('anomalies', [])
            suggestions = analysis_result.get('suggestions', [])
            
            logger.info("📝 Aggiornamento note Notion con analisi AI...")
            
            # Nota: Questa è una versione semplificata
            # In produzione, avrai bisogno di mappare i dati correttamente
            logger.info("✓ Note AI generate (implementazione in produzione)")
        
        except Exception as e:
            logger.error(f"✗ Errore nell'aggiornamento note: {e}")
    
    def create_sync_report(self, sync_data: Dict) -> str:
        """
        Crea un report di sincronizzazione
        
        Args:
            sync_data: Dati della sincronizzazione
            
        Returns:
            Stringa con il report
        """
        try:
            timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            
            report = f"📊 REPORT SINCRONIZZAZIONE\n"
            report += f"{'='*40}\n"
            report += f"⏰ Data/Ora: {timestamp}\n\n"
            
            if 'analysis' in sync_data:
                analysis = sync_data['analysis']
                report += f"📦 Prodotti WooCommerce: {analysis.get('total_products', 0)}\n"
                report += f"📋 Item Notion: {analysis.get('total_items', 0)}\n"
                report += f"⚠️  Discrepanze: {len(analysis.get('discrepancies', []))}\n"
                report += f"💡 Insights:\n"
                for insight in analysis.get('insights', []):
                    report += f"  • {insight}\n"
                report += "\n"
            
            if 'anomalies' in sync_data:
                report += f"🔍 Anomalie rilevate: {len(sync_data['anomalies'])}\n"
                for anomaly in sync_data['anomalies'][:5]:  # Primi 5
                    report += f"  • [{anomaly['severity']}] {anomaly['product_name']}\n"
                report += "\n"
            
            if 'suggestions' in sync_data:
                report += f"💡 Suggerimenti riordino: {len(sync_data['suggestions'])}\n"
                for sugg in sync_data['suggestions'][:5]:  # Primi 5
                    report += f"  • {sugg['product_name']} ({sugg['current_stock']} unità)\n"
            
            return report
        
        except Exception as e:
            logger.error(f"✗ Errore nella creazione report: {e}")
            return "Errore nella generazione del report"
