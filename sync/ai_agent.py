import os
from loguru import logger
from typing import Dict, List
from datetime import datetime

class AIAgent:
    """Agent AI per analisi intelligente dello stock e rilevamento anomalie"""
    
    def __init__(self):
        """Inizializza l'AI Agent"""
        # Nota: Puoi integrare OpenAI, Anthropic o altri LLM
        # Per ora, implemento logica intelligente senza API esterna
        self.model = os.getenv('AI_MODEL', 'local')
        logger.info(f"✓ AI Agent inizializzato (Modalità: {self.model})")
    
    def analyze_stock_discrepancies(self, woo_products: List[Dict], notion_items: List[Dict]) -> Dict:
        """
        Analizza le discrepanze di stock tra WooCommerce e Notion
        
        Args:
            woo_products: Lista prodotti WooCommerce
            notion_items: Lista item Notion
            
        Returns:
            Dict con analisi delle discrepanze
        """
        try:
            discrepancies = []
            summary = {
                "total_products": len(woo_products),
                "total_items": len(notion_items),
                "discrepancies": [],
                "warnings": [],
                "insights": []
            }
            
            # Crea mappa SKU -> prodotto WooCommerce
            woo_map = {p.get('sku', ''): p for p in woo_products if p.get('sku')}
            
            for item in notion_items:
                sku = self._extract_sku(item)
                stock_notion = self._extract_stock(item)
                
                if not sku:
                    continue
                
                woo_product = woo_map.get(sku)
                
                if woo_product:
                    stock_woo = woo_product.get('stock_quantity', 0)
                    
                    # Analizza discrepanze
                    if stock_notion != stock_woo:
                        discrepancy = {
                            "sku": sku,
                            "product_name": woo_product.get('name'),
                            "stock_woo": stock_woo,
                            "stock_notion": stock_notion,
                            "difference": abs(stock_notion - stock_woo),
                            "severity": self._calculate_severity(stock_woo, stock_notion)
                        }
                        discrepancies.append(discrepancy)
                else:
                    summary["warnings"].append(f"⚠️  SKU {sku} trovato in Notion ma non in WooCommerce")
            
            summary["discrepancies"] = discrepancies
            
            # Genera insights
            summary["insights"] = self._generate_insights(woo_products, notion_items)
            
            logger.info(f"✓ Analisi completata: {len(discrepancies)} discrepanze rilevate")
            return summary
            
        except Exception as e:
            logger.error(f"✗ Errore nell'analisi discrepanze: {e}")
            return {"error": str(e)}
    
    def detect_anomalies(self, products: List[Dict]) -> List[Dict]:
        """
        Rileva anomalie nei dati dei prodotti
        
        Args:
            products: Lista prodotti da analizzare
            
        Returns:
            Lista anomalie rilevate
        """
        try:
            anomalies = []
            
            for product in products:
                product_id = product.get('id')
                name = product.get('name', 'Unknown')
                stock = product.get('stock_quantity') or 0  # Converte None a 0
                price = product.get('price') or 0  # Converte None a 0
                
                # Anomalia: Stock negativo
                if stock < 0:
                    anomalies.append({
                        "type": "NEGATIVE_STOCK",
                        "severity": "CRITICAL",
                        "product_id": product_id,
                        "product_name": name,
                        "message": f"Stock negativo: {stock}",
                        "recommendation": "Verifica immediata del database WooCommerce"
                    })
                
                # Anomalia: Stock zero con prodotto attivo
                if stock == 0 and product.get('status') == 'publish':
                    anomalies.append({
                        "type": "OUT_OF_STOCK",
                        "severity": "HIGH",
                        "product_id": product_id,
                        "product_name": name,
                        "message": "Prodotto esaurito ma ancora attivo",
                        "recommendation": "Considera di disattivare il prodotto o effettuare un ordine"
                    })
                
                # Anomalia: Prezzo nullo
                if not price or float(price) == 0:
                    anomalies.append({
                        "type": "MISSING_PRICE",
                        "severity": "MEDIUM",
                        "product_id": product_id,
                        "product_name": name,
                        "message": "Prezzo non impostato",
                        "recommendation": "Configura il prezzo del prodotto"
                    })
                
                # Anomalia: Stock molto alto (possibile errore di sincronizzazione)
                if stock > 10000:
                    anomalies.append({
                        "type": "UNUSUAL_STOCK",
                        "severity": "MEDIUM",
                        "product_id": product_id,
                        "product_name": name,
                        "message": f"Stock insolitamente alto: {stock}",
                        "recommendation": "Verifica se è un errore di sincronizzazione"
                    })
            
            if anomalies:
                logger.warning(f"⚠️  {len(anomalies)} anomalie rilevate")
            else:
                logger.info("✓ Nessuna anomalia rilevata")
            
            return anomalies
            
        except Exception as e:
            logger.error(f"✗ Errore nel rilevamento anomalie: {e}")
            return []
    
    def generate_reorder_suggestions(self, products: List[Dict], threshold: int = 10) -> List[Dict]:
        """
        Genera suggerimenti intelligenti di riordino
        
        Args:
            products: Lista prodotti
            threshold: Soglia di stock per suggerire riordino
            
        Returns:
            Lista suggerimenti di riordino
        """
        try:
            suggestions = []
            
            for product in products:
                stock = product.get('stock_quantity') or 0  # Converte None a 0
                name = product.get('name', 'Unknown')
                product_id = product.get('id')
                
                if 0 < stock <= threshold:
                    suggestion = {
                        "product_id": product_id,
                        "product_name": name,
                        "current_stock": stock,
                        "threshold": threshold,
                        "urgency": self._calculate_urgency(stock, threshold),
                        "recommended_order": max(50, threshold * 3),
                        "message": f"Stock basso ({stock} unità), consigliato riordino"
                    }
                    suggestions.append(suggestion)
            
            if suggestions:
                logger.info(f"💡 {len(suggestions)} suggerimenti di riordino generati")
            
            return suggestions
            
        except Exception as e:
            logger.error(f"✗ Errore nella generazione suggerimenti: {e}")
            return []
    
    def generate_intelligent_notes(self, product: Dict, context: Dict) -> str:
        """
        Genera note intelligenti per il prodotto basate su analisi
        
        Args:
            product: Dati del prodotto
            context: Contesto aggiuntivo (anomalie, discrepanze, etc.)
            
        Returns:
            Note intelligenti in formato stringa
        """
        try:
            notes = []
            timestamp = datetime.now().strftime("%d/%m/%Y %H:%M")
            
            notes.append(f"🔄 [Sincronizzazione {timestamp}]")
            
            stock = product.get('stock_quantity', 0)
            name = product.get('name', 'Unknown')
            
            # Nota su stato dello stock
            if stock == 0:
                notes.append("⚠️  Prodotto esaurito")
            elif stock < 10:
                notes.append(f"⏰ Stock critico ({stock} unità)")
            elif stock > 100:
                notes.append(f"✅ Stock abbondante ({stock} unità)")
            else:
                notes.append(f"ℹ️  Stock disponibile ({stock} unità)")
            
            # Nota su anomalie
            if context.get('anomalies'):
                for anomaly in context['anomalies']:
                    if anomaly['product_id'] == product.get('id'):
                        notes.append(f"🔍 {anomaly['message']}")
            
            # Nota su suggerimenti
            if context.get('suggestions'):
                for suggestion in context['suggestions']:
                    if suggestion['product_id'] == product.get('id'):
                        notes.append(f"💡 {suggestion['message']}")
            
            return " | ".join(notes)
            
        except Exception as e:
            logger.error(f"✗ Errore nella generazione note: {e}")
            return f"Errore nell'analisi ({str(e)})"
    
    def _calculate_severity(self, stock_woo: int, stock_notion: int) -> str:
        """Calcola la gravità della discrepanza"""
        difference = abs(stock_woo - stock_notion)
        if difference > 100:
            return "CRITICAL"
        elif difference > 50:
            return "HIGH"
        elif difference > 10:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _calculate_urgency(self, stock: int, threshold: int) -> str:
        """Calcola l'urgenza del riordino"""
        if stock <= threshold * 0.25:
            return "CRITICAL"
        elif stock <= threshold * 0.5:
            return "HIGH"
        else:
            return "MEDIUM"
    
    def _generate_insights(self, woo_products: List[Dict], notion_items: List[Dict]) -> List[str]:
        """Genera insight intelligenti sui dati"""
        insights = []
        
        try:
            # Calcola medie di stock
            woo_stocks = [p.get('stock_quantity', 0) for p in woo_products if p.get('sku')]
            if woo_stocks:
                avg_stock = sum(woo_stocks) / len(woo_stocks)
                insights.append(f"📊 Stock medio WooCommerce: {avg_stock:.0f} unità")
            
            # Prodotti esauriti
            out_of_stock = len([p for p in woo_products if p.get('stock_quantity', 0) <= 0])
            if out_of_stock > 0:
                insights.append(f"📦 {out_of_stock} prodotti esauriti")
            
            # Tasso di sincronizzazione
            if len(notion_items) > 0:
                sync_rate = (len([p for p in woo_products if p.get('sku')]) / len(notion_items)) * 100
                insights.append(f"🔄 Tasso di sincronizzazione: {sync_rate:.1f}%")
        
        except Exception as e:
            logger.warning(f"⚠️  Errore nella generazione insight: {e}")
        
        return insights
    
    def _extract_sku(self, notion_item: Dict) -> str:
        """Estrae SKU da item Notion"""
        try:
            properties = notion_item.get('properties', {})
            sku_prop = properties.get('SKU', {})
            if sku_prop.get('type') == 'rich_text':
                return sku_prop.get('rich_text', [{}])[0].get('text', {}).get('content', '')
            return ''
        except:
            return ''
    
    def _extract_stock(self, notion_item: Dict) -> int:
        """Estrae stock da item Notion"""
        try:
            properties = notion_item.get('properties', {})
            stock_prop = properties.get('Stock', {})
            if stock_prop.get('type') == 'number':
                return int(stock_prop.get('number', 0) or 0)
            return 0
        except:
            return 0
