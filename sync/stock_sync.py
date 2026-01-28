from loguru import logger
from typing import Dict, List

class StockSynchronizer:
    """Sincronizzatore di stock tra WooCommerce e Notion"""
    
    def __init__(self, woo_client, notion_client):
        """
        Inizializza il sincronizzatore
        
        Args:
            woo_client: Client WooCommerce
            notion_client: Client Notion
        """
        self.woo = woo_client
        self.notion = notion_client
    
    def sync(self):
        """Esegue la sincronizzazione completa dello stock"""
        try:
            logger.info("🔄 Inizio sincronizzazione...")
            
            # Sincronizza da Notion a WooCommerce (priorità alle modifiche manuali su Notion)
            self._sync_notion_to_woo()
            
            # Sincronizza da WooCommerce a Notion (sincronizza nuovi prodotti e aggiornamenti da WooCommerce)
            self._sync_woo_to_notion()
            
            logger.info("✓ Sincronizzazione completata")
        except Exception as e:
            logger.error(f"✗ Errore durante la sincronizzazione: {e}", exc_info=True)
            raise
    
    def _extract_categories(self, product: Dict) -> str:
        """
        Estrae la prima categoria del prodotto dalla chiave 'categories'
        (Category in Notion è un Select, quindi può avere un solo valore)
        
        Args:
            product: Dati del prodotto da WooCommerce
            
        Returns:
            Prima categoria o stringa vuota
        """
        if product.get('categories'):
            categories_list = product.get('categories', [])
            if categories_list and isinstance(categories_list, list):
                first_category = categories_list[0].get('name', '').strip()
                if first_category:
                    return first_category
        return ""
    
    def _extract_brand(self, product: Dict) -> str:
        """
        Estrae il brand/marca del prodotto da metadati o attributi
        
        Args:
            product: Dati del prodotto da WooCommerce
            
        Returns:
            Brand string
        """
        product_name = product.get('name', 'Sconosciuto')
        product_id = product.get('id', 'N/A')
        brand = ""
        
        # 1. Cerca in brands (PRIMA PRIORITÀ - dalla risposta API di WooCommerce)
        if product.get('brands'):
            brands_list = product.get('brands', [])
            if brands_list and isinstance(brands_list, list):
                brand_name = brands_list[0].get('name', '').strip()
                if brand_name:
                    return brand_name
        
        # 2. Cerca nei metadati del prodotto (custom fields) - SECONDA PRIORITÀ
        if product.get('meta_data'):
            for meta in product.get('meta_data', []):
                key = meta.get('key', '').lower()
                if any(b in key for b in ['brand', 'marca', 'marchio', 'marchi', 'manufacturer']):
                    value = meta.get('value', '').strip()
                    if value:
                        return value
        
        # 3. Cerca negli attributi (TERZA PRIORITÀ)
        if product.get('attributes'):
            for attr in product.get('attributes', []):
                attr_name = attr.get('name', '').lower()
                if any(b in attr_name for b in ['brand', 'marca', 'marchio', 'marchi', 'manufacturer', 'produttore']):
                    value = attr.get('option', '').strip()
                    if value:
                        return value
        
        # Se non trovo il brand, restituisci stringa vuota
        return brand
    
    def _sync_woo_to_notion(self):
        """Sincronizza i prodotti (e varianti) da WooCommerce a Notion"""
        try:
            logger.debug("📤 Sincronizzazione WooCommerce → Notion...")
            
            woo_products = self.woo.get_products(include_variants=True)
            synced_count = 0
            synced_skus = set()  # Traccia gli SKU già sincronizzati per evitare duplicati
            
            for product in woo_products:
                try:
                    product_id = product.get('id')
                    product_name = product.get('name', 'N/A')
                    product_type = product.get('type', 'simple')
                    sku = product.get('_sku')
                    
                    # Normalizza lo SKU (trim e lowercase per confronti)
                    sku_normalized = (sku.strip() if sku else "").lower()
                    
                    # Controlla se lo SKU è già stato sincronizzato in questa sessione
                    if sku_normalized and sku_normalized in synced_skus:
                        logger.warning(f"⊘ Duplicato rilevato: {product_name} ({sku}) - SKU già sincronizzato")
                        continue
                    
                    stock = product.get('stock_quantity', 0)
                    price = product.get('price', product.get('regular_price', ''))
                    brand = self._extract_brand(product)
                    categories = self._extract_categories(product)
                    variants = product.get('_variants', [])
                    
                    # Se è un prodotto variabile CON varianti, sincronizza SOLO le varianti, NON il padre
                    if product_type == 'variable' and variants:
                        logger.debug(f"⊘ Prodotto variabile {product_name} - sincronizzerò solo le {len(variants)} varianti")
                    else:
                        # Sincronizza il prodotto principale (semplice o variabile senza varianti)
                        notion_item = self.notion.get_item_by_sku(sku)
                        
                        if notion_item:
                            # Se il prodotto esiste in Notion, applica logica del minore
                            page_id = notion_item['id']
                            existing_stock = self.notion.extract_property(notion_item, 'Stock')
                            
                            # Usa il minore tra stock Notion e WooCommerce (previene aumento accidentale)
                            update_stock = min(existing_stock if existing_stock is not None else stock, stock)
                            
                            # Aggiorna Notion se lo stock calcolato è diverso da quello esistente
                            if update_stock != existing_stock:
                                self.notion.update_item_stock(page_id, update_stock, brand, price, categories)
                                logger.info(f"✓ Aggiornato (stock minore): {product_name} ({sku}) Stock: {update_stock} (Notion: {existing_stock}, WooCommerce: {stock}), Brand: {brand}")
                            else:
                                # Se lo stock è uguale, aggiorna solo i campi metadata
                                self.notion.update_item_stock(page_id, update_stock, brand, price, categories)
                                logger.debug(f"✓ Aggiornato (metadata): {product_name} ({sku}), Brand: {brand}, Prezzo: {price}")
                            
                            # Traccia lo SKU come già sincronizzato
                            if sku_normalized:
                                synced_skus.add(sku_normalized)
                        else:
                            # Crea item in Notion
                            logger.info(f"📝 Creazione item Notion: {product_name} ({sku})")
                            properties = self._build_notion_properties(product_name, sku, stock, brand, price, categories)
                            self.notion.create_item(properties)
                            logger.info(f"✓ Creato: {product_name} ({sku})")
                            synced_count += 1
                            
                            # Traccia lo SKU come sincronizzato
                            if sku_normalized:
                                synced_skus.add(sku_normalized)
                            
                            # Se lo SKU era generato, aggiorna anche WooCommerce
                            if sku.startswith('ADIVO-'):
                                try:
                                    self.woo.update_product_data(sku, {"sku": sku})
                                    logger.debug(f"✓ SKU aggiornato su WooCommerce: {sku}")
                                except Exception as e:
                                    logger.warning(f"⚠️  Non posso aggiornare SKU su WooCommerce: {e}")
                    
                    # Sincronizza varianti se presenti
                    for variant in variants:
                        try:
                            variant_sku = variant.get('_sku')
                            variant_stock = variant.get('stock_quantity', 0)
                            variant_name = variant.get('_product_name', product_name)
                            variant_price = variant.get('price', variant.get('regular_price', price))
                            
                            # Normalizza lo SKU della variante
                            variant_sku_normalized = (variant_sku.strip() if variant_sku else "").lower()
                            
                            # Controlla se lo SKU della variante è già stato sincronizzato
                            if variant_sku_normalized and variant_sku_normalized in synced_skus:
                                logger.warning(f"⊘ Duplicato variante rilevato: {variant_name} ({variant_sku}) - SKU già sincronizzato")
                                continue
                            
                            variant_item = self.notion.get_item_by_sku(variant_sku)
                            
                            if variant_item:
                                page_id = variant_item['id']
                                existing_variant_stock = self.notion.extract_property(variant_item, 'Stock')
                                
                                # Usa il minore tra stock Notion e WooCommerce (previene aumento accidentale)
                                update_variant_stock = min(existing_variant_stock if existing_variant_stock is not None else variant_stock, variant_stock)
                                
                                # Aggiorna Notion se lo stock calcolato è diverso da quello esistente
                                if update_variant_stock != existing_variant_stock:
                                    self.notion.update_item_stock(page_id, update_variant_stock, brand, variant_price, categories)
                                    logger.info(f"✓ Aggiornato variante (stock minore): {variant_name} ({variant_sku}) Stock: {update_variant_stock} (Notion: {existing_variant_stock}, WooCommerce: {variant_stock})")
                                else:
                                    # Se lo stock è uguale, aggiorna solo i campi metadata
                                    self.notion.update_item_stock(page_id, update_variant_stock, brand, variant_price, categories)
                                    logger.debug(f"✓ Aggiornato variante (metadata): {variant_name} ({variant_sku})")
                                
                                # Traccia lo SKU della variante come già sincronizzato
                                if variant_sku_normalized:
                                    synced_skus.add(variant_sku_normalized)
                            else:
                                logger.info(f"📝 Creazione variante Notion: {variant_name} ({variant_sku})")
                                properties = self._build_notion_properties(variant_name, variant_sku, variant_stock, brand, variant_price, categories)
                                self.notion.create_item(properties)
                                logger.info(f"✓ Creata variante: {variant_name}")
                                synced_count += 1
                                
                                # Traccia lo SKU della variante come sincronizzato
                                if variant_sku_normalized:
                                    synced_skus.add(variant_sku_normalized)
                                
                                # Se lo SKU era generato, aggiorna anche WooCommerce
                                if variant_sku.startswith('ADIVO-'):
                                    try:
                                        self.woo.update_product_data(variant_sku, {"sku": variant_sku})
                                        logger.debug(f"✓ SKU variante aggiornato su WooCommerce: {variant_sku}")
                                    except Exception as e:
                                        logger.warning(f"⚠️  Non posso aggiornare SKU variante su WooCommerce: {e}")
                        except Exception as e:
                            logger.error(f"✗ Errore sincronizzazione variante {variant_sku}: {e}")
                            continue
                
                except Exception as e:
                    logger.error(f"✗ Errore sincronizzazione prodotto {product_id}: {e}")
                    continue
            
            logger.info(f"✓ Sincronizzazione WooCommerce → Notion completata ({synced_count} creazioni)")
        except Exception as e:
            logger.error(f"✗ Errore nella sincronizzazione WooCommerce → Notion: {e}")
            raise
    
    def _build_notion_properties(self, name: str, sku: str, stock: int, brand: str = "", price: str = "", categories: str = "") -> Dict:
        """
        Costruisce le proprietà per un item Notion
        
        Args:
            name: Nome del prodotto
            sku: SKU univoco
            stock: Quantità stock
            brand: Brand/Marca del prodotto
            price: Prezzo del prodotto (come stringa o numero)
            categories: Categorie del prodotto (come stringa comma-separated)
            
        Returns:
            Dict con proprietà formattate per Notion
        """
        properties = {
            "Name": {
                "title": [{"text": {"content": name}}]
            },
            "SKU": {
                "rich_text": [{"text": {"content": sku}}]
            },
            "Stock": {
                "number": stock
            }
        }
        
        # Aggiungi Brand se presente
        if brand:
            properties["Brand"] = {
                "rich_text": [{"text": {"content": brand}}]
            }
        
        # Aggiungi Prezzo se presente (come numero)
        if price:
            try:
                price_float = float(str(price))
                properties["Price"] = {
                    "number": price_float
                }
            except (ValueError, TypeError):
                logger.warning(f"⚠️  Prezzo non valido: {price}")
        
        # Aggiungi Category se presente (come Select)
        if categories:
            properties["Category"] = {
                "select": {
                    "name": categories
                }
            }
        
        return properties
    
    def _sync_notion_to_woo(self):
        """Sincronizza i prodotti da Notion a WooCommerce"""
        try:
            logger.debug("📥 Sincronizzazione Notion → WooCommerce...")
            
            notion_items = self.notion.get_all_items()
            synced_count = 0
            
            for item in notion_items:
                try:
                    # Estrae le proprietà
                    sku = self.notion.extract_property(item, 'SKU')
                    notion_stock = self.notion.extract_property(item, 'Stock')
                    name = self.notion.extract_property(item, 'Name')
                    
                    if not sku or notion_stock is None:
                        logger.debug(f"⚠️  Item Notion senza SKU o Stock - Skipped")
                        continue
                    
                    # Cerca il prodotto WooCommerce tramite SKU (supporta prodotti e varianti)
                    woo_product = self.woo.get_product_by_sku(sku)
                    
                    if woo_product:
                        # Sincronizza il valore di Notion a WooCommerce SENZA minore
                        # L'utente ha modificato Notion di proposito, va rispettato
                        woo_stock = woo_product.get('stock_quantity', 0) or 0
                        
                        # Aggiorna WooCommerce sempre con il valore di Notion
                        if notion_stock != woo_stock:
                            self.woo.update_product_stock(sku, int(notion_stock))
                            logger.info(f"✓ Sincronizzato Notion → WooCommerce: {name} ({sku}) Stock: {notion_stock} (da Notion: {notion_stock}, era WooCommerce: {woo_stock})")
                        else:
                            logger.debug(f"✓ Stock già sincronizzato: {name} ({sku}) = {notion_stock}")
                        synced_count += 1
                    else:
                        logger.debug(f"ℹ️  Prodotto WooCommerce non trovato per SKU: {sku}")
                
                except Exception as e:
                    logger.error(f"✗ Errore nel sincronizzare item Notion ({sku}): {e}")
                    continue
            
            logger.info(f"✓ Sincronizzazione Notion → WooCommerce completata ({synced_count} aggiornamenti)")
        except Exception as e:
            logger.error(f"✗ Errore nella sincronizzazione Notion → WooCommerce: {e}")
            raise
    
    def get_sync_status(self) -> Dict:
        """Ritorna lo stato della sincronizzazione"""
        return {
            "woocommerce": "connected",
            "notion": "connected",
            "status": "ready"
        }
