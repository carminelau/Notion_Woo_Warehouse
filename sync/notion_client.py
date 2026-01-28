from notion_client import Client
from loguru import logger
from typing import List, Dict

class NotionClient:
    """Client per interagire con il database Notion"""
    
    def __init__(self, token, database_id):
        """
        Inizializza il client Notion
        
        Args:
            token: Token di autenticazione Notion
            database_id: ID del database Notion
        """
        self.token = token
        self.database_id = database_id
        
        try:
            self.client = Client(auth=token)
            logger.info("✓ Notion API connessa con successo")
        except Exception as e:
            logger.error(f"✗ Errore nella connessione a Notion: {e}")
            raise
    
    def get_all_items(self) -> List[Dict]:
        """Recupera tutti gli item dal database Notion"""
        try:
            logger.debug("📥 Recupero item da Notion...")
            items = []
            has_more = True
            start_cursor = None
            
            while has_more:
                response = self.client.databases.query(
                    database_id=self.database_id,
                    start_cursor=start_cursor
                )
                
                items.extend(response.get('results', []))
                has_more = response.get('has_more', False)
                start_cursor = response.get('next_cursor')
            
            logger.info(f"✓ Recuperati {len(items)} item da Notion")
            return items
        except Exception as e:
            logger.error(f"✗ Errore nel recupero degli item: {e}")
            raise
    
    def get_item_by_sku(self, sku: str):
        """
        Recupera un item dal database usando lo SKU
        Normalizza lo SKU (trim e case-insensitive) per evitare duplicati
        """
        try:
            # Normalizza lo SKU per la ricerca
            sku_normalized = sku.strip() if sku else ""
            
            if not sku_normalized:
                logger.warning("⚠️  SKU vuoto - impossibile cercare item")
                return None
            
            logger.info(f"🔍 Ricerca item con SKU: '{sku_normalized}'")
            
            # Primo tentativo: ricerca esatta
            response = self.client.databases.query(
                database_id=self.database_id,
                filter={
                    "property": "SKU",
                    "rich_text": {
                        "equals": sku_normalized
                    }
                }
            )
            
            if response['results']:
                found_item = response['results'][0]
                logger.info(f"✓ Trovato item esatto per SKU: {sku_normalized}")
                return found_item
            
            # Se non trovato con ricerca esatta, recupera tutti gli item e cerca manualmente
            logger.info(f"⚠️  SKU esatto non trovato '{sku_normalized}', ricerca manuale tra tutti gli item...")
            all_items = self.get_all_items()
            
            for item in all_items:
                try:
                    item_sku = self.extract_property(item, 'SKU')
                    if item_sku:
                        item_sku_normalized = item_sku.strip().lower()
                        search_sku_normalized = sku_normalized.lower()
                        if item_sku_normalized == search_sku_normalized:
                            logger.info(f"✓ Trovato item con SKU normalizzato: '{sku_normalized}' (match: '{item_sku}')")
                            return item
                except Exception as e:
                    logger.debug(f"⚠️  Errore nell'estrazione SKU da item: {e}")
                    continue
            
            logger.warning(f"✗ Item NON trovato per SKU: '{sku_normalized}' - verrà creato nuovo item")
            return None
            
        except Exception as e:
            logger.error(f"✗ Errore nel recupero dell'item per SKU: {e}")
            return None
    
    def update_item_stock(self, page_id: str, quantity: int, brand: str = "", price: str = "", categories: str = ""):
        """
        Aggiorna lo stock (e opzionalmente brand, prezzo e categorie) di un item
        
        Args:
            page_id: ID della pagina Notion
            quantity: Nuova quantità di stock
            brand: Brand del prodotto (opzionale)
            price: Prezzo del prodotto (opzionale, come stringa o numero)
            categories: Categorie del prodotto (opzionale, come stringa comma-separated)
        """
        try:
            update_data = {
                "Stock": {
                    "number": quantity
                }
            }
            
            # Aggiungi Brand se fornito
            if brand:
                update_data["Brand"] = {
                    "rich_text": [{"text": {"content": brand}}]
                }
            
            # Aggiungi Prezzo se fornito (come numero)
            if price:
                try:
                    price_float = float(str(price))
                    update_data["Price"] = {
                        "number": price_float
                    }
                except (ValueError, TypeError):
                    logger.warning(f"⚠️  Prezzo non valido per aggiornamento: {price}")
            
            # Aggiungi Category se fornita (come Select)
            if categories:
                update_data["Category"] = {
                    "select": {
                        "name": categories
                    }
                }
            
            self.client.pages.update(
                page_id=page_id,
                properties=update_data
            )
            log_msg = f"✓ Stock Notion aggiornato - Page {page_id}: {quantity} unità"
            if brand:
                log_msg += f", Brand: {brand}"
            if price:
                log_msg += f", Prezzo: {price}"
            if categories:
                log_msg += f", Categorie: {categories}"
            logger.info(log_msg)
        except Exception as e:
            logger.error(f"✗ Errore nell'aggiornamento dello stock Notion: {e}")
            raise
    
    def create_item(self, properties: Dict):
        """
        Crea un nuovo item nel database Notion
        
        Args:
            properties: Proprietà dell'item
        """
        try:
            page = self.client.pages.create(
                parent={"database_id": self.database_id},
                properties=properties
            )
            logger.info(f"✓ Nuovo item creato in Notion: {page['id']}")
            return page
        except Exception as e:
            logger.error(f"✗ Errore nella creazione dell'item: {e}")
            raise
    
    def extract_property(self, page: Dict, property_name: str):
        """Estrae il valore di una proprietà da una pagina Notion"""
        try:
            prop = page['properties'].get(property_name, {})
            prop_type = prop.get('type')
            
            if prop_type == 'title':
                return prop.get('title', [{}])[0].get('text', {}).get('content', '')
            elif prop_type == 'rich_text':
                return prop.get('rich_text', [{}])[0].get('text', {}).get('content', '')
            elif prop_type == 'number':
                return prop.get('number', 0)
            elif prop_type == 'select':
                return prop.get('select', {}).get('name', '')
            else:
                return None
        except Exception as e:
            logger.warning(f"⚠️  Errore nell'estrazione della proprietà {property_name}: {e}")
            return None
