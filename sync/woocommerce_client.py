from loguru import logger
from woocommerce import API
import os
import time
import hashlib

class WooCommerceClient:
    """Client per interagire con l'API di WooCommerce"""
    
    def __init__(self, api_url, consumer_key, consumer_secret):
        """
        Inizializza il client WooCommerce
        
        Args:
            api_url: URL della WooCommerce store (es. https://mystore.com)
            consumer_key: Chiave consumer dell'API
            consumer_secret: Secret consumer dell'API
        """
        self.api_url = api_url.rstrip('/')
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.timeout = int(os.getenv('WOOCOMMERCE_TIMEOUT', 30))
        self.max_retries = int(os.getenv('WOOCOMMERCE_MAX_RETRIES', 3))
        
        try:
            self.client = API(
                url=self.api_url,
                consumer_key=consumer_key,
                consumer_secret=consumer_secret,
                version="wc/v3",
                timeout=self.timeout
            )
            logger.info(f"✓ WooCommerce API connessa con successo (timeout: {self.timeout}s)")
        except Exception as e:
            logger.error(f"✗ Errore nella connessione a WooCommerce: {e}")
            raise
    
    def _generate_sku(self, product_id, variant_id=None):
        """
        Genera uno SKU univoco basato su ID prodotto e variante con prefisso ADIVO-
        
        Args:
            product_id: ID del prodotto
            variant_id: ID della variante (opzionale)
            
        Returns:
            SKU generato (formato: ADIVO-{product_id} o ADIVO-{product_id}-V{variant_id})
        """
        if variant_id:
            sku = f"ADIVO-{product_id}-V{variant_id}"
        else:
            sku = f"ADIVO-{product_id}"
        return sku
    
    def _retry_request(self, method, endpoint, data=None, params=None):
        """
        Esegue una richiesta con retry logic e backoff esponenziale
        
        Args:
            method: Metodo HTTP ('get', 'put', 'post')
            endpoint: Endpoint API
            data: Dati per PUT/POST
            params: Query parameters per GET
        """
        for attempt in range(self.max_retries):
            try:
                response = None
                if method.lower() == 'get':
                    response = self.client.get(endpoint, params=params)
                elif method.lower() == 'put':
                    response = self.client.put(endpoint, data)
                elif method.lower() == 'post':
                    response = self.client.post(endpoint, data)
                
                # Converti Response object in lista/dict
                if hasattr(response, 'json'):
                    try:
                        return response.json()
                    except:
                        return response
                return response
                
            except (TimeoutError, ConnectionError) as e:
                wait_time = 2 ** attempt  # Backoff esponenziale: 1s, 2s, 4s
                if attempt < self.max_retries - 1:
                    logger.warning(f"⏱️  Timeout WooCommerce (attempt {attempt+1}/{self.max_retries}), retry tra {wait_time}s... ({e})")
                    time.sleep(wait_time)
                else:
                    logger.error(f"✗ Errore WooCommerce dopo {self.max_retries} tentativi: {e}")
                    raise
    
    def get_products(self, include_variants=True):
        """
        Recupera tutti i prodotti da WooCommerce, including varianti
        
        Args:
            include_variants: Se True, include anche le varianti dei prodotti variabili
            
        Returns:
            Lista di prodotti con varianti (se presenti)
        """
        try:
            logger.debug("📥 Recupero prodotti da WooCommerce...")
            products_response = self._retry_request('get', 'products', params={"per_page": 100})
            
            if not products_response:
                return []
            
            products = products_response if isinstance(products_response, list) else [products_response]
            all_products = []
            
            for product in products:
                product_type = product.get('type', 'simple')
                product['_sku'] = product.get('sku') or self._generate_sku(product.get('id'))
                
                if product_type == 'variable' and include_variants:
                    # Recupera le varianti
                    try:
                        variants = self._retry_request(
                            'get', 
                            f"products/{product.get('id')}/variations",
                            params={"per_page": 100}
                        )
                        variants = variants if isinstance(variants, list) else [variants]
                        
                        product['_variants'] = []
                        for variant in variants:
                            variant['_sku'] = variant.get('sku') or self._generate_sku(product.get('id'), variant.get('id'))
                            variant['_product_name'] = f"{product.get('name')} - {variant.get('attributes', [{}])[0].get('option', 'Variante')}"
                            product['_variants'].append(variant)
                        
                        logger.debug(f"✓ Recuperate {len(product['_variants'])} varianti per prodotto {product.get('name')}")
                    except Exception as e:
                        logger.warning(f"⚠️  Non posso recuperare varianti per {product.get('name')}: {e}")
                        product['_variants'] = []
                else:
                    product['_variants'] = []
                
                all_products.append(product)
            
            logger.info(f"✓ Recuperati {len(all_products)} prodotti (con varianti) da WooCommerce")
            return all_products
        except Exception as e:
            logger.error(f"✗ Errore nel recupero dei prodotti: {e}")
            raise
    
    def get_product_by_sku(self, sku):
        """
        Recupera un prodotto o variante tramite SKU
        
        Args:
            sku: SKU da cercare
            
        Returns:
            Dict con prodotto/variante o None
        """
        try:
            # Controlla se è uno SKU generato automaticamente per variante
            if sku.startswith('ADIVO-') and '-V' in sku:
                # Formato: ADIVO-{product_id}-V{variant_id}
                parts = sku.replace('ADIVO-', '').split('-V')
                product_id = parts[0]
                variant_id = parts[1]
                
                try:
                    variant = self._retry_request('get', f"products/{product_id}/variations/{variant_id}")
                    if variant:
                        variant['_sku'] = sku
                        return variant
                except:
                    pass
            elif sku.startswith('ADIVO-'):
                # Formato: ADIVO-{product_id}
                product_id = sku.replace('ADIVO-', '')
                try:
                    product = self._retry_request('get', f"products/{product_id}")
                    if product:
                        product['_sku'] = sku
                        return product
                except:
                    pass
            
            # Ricerca standard per SKU custom
            products = self._retry_request('get', 'products', params={"sku": sku})
            if products:
                products[0]['_sku'] = sku
                return products[0]
            
            return None
        except Exception as e:
            logger.error(f"✗ Errore nel recupero del prodotto per SKU {sku}: {e}")
            return None
    
    def update_product_stock(self, sku, quantity):
        """
        Aggiorna lo stock di un prodotto o variante tramite SKU
        
        Args:
            sku: SKU del prodotto/variante
            quantity: Nuova quantità di stock
        """
        try:
            product = self.get_product_by_sku(sku)
            
            if not product:
                logger.warning(f"⚠️  Prodotto con SKU {sku} non trovato")
                return None
            
            # Determina se è una variante
            if sku.startswith('ADIVO-') and '-V' in sku:
                parts = sku.replace('ADIVO-', '').split('-V')
                product_id = parts[0]
                variant_id = parts[1]
                
                data = {"stock_quantity": quantity}
                response = self._retry_request('put', f"products/{product_id}/variations/{variant_id}", data=data)
                logger.info(f"✓ Stock variante aggiornato - SKU {sku}: {quantity} unità")
                return response
            else:
                product_id = product.get('id')
                data = {"stock_quantity": quantity}
                response = self._retry_request('put', f"products/{product_id}", data=data)
                logger.info(f"✓ Stock prodotto aggiornato - SKU {sku}: {quantity} unità")
                return response
        except Exception as e:
            logger.error(f"✗ Errore nell'aggiornamento dello stock per SKU {sku}: {e}")
            raise
    
    def update_product_data(self, sku, data_dict):
        """
        Aggiorna dati generici di un prodotto o variante tramite SKU
        
        Args:
            sku: SKU del prodotto/variante
            data_dict: Dict con dati da aggiornare (es: {"sku": "ADIVO-123", "regular_price": "19.99"})
        """
        try:
            product = self.get_product_by_sku(sku)
            
            if not product:
                logger.warning(f"⚠️  Prodotto con SKU {sku} non trovato")
                return None
            
            # Determina se è una variante
            if sku.startswith('ADIVO-') and '-V' in sku:
                parts = sku.replace('ADIVO-', '').split('-V')
                product_id = parts[0]
                variant_id = parts[1]
                
                response = self._retry_request('put', f"products/{product_id}/variations/{variant_id}", data=data_dict)
                logger.debug(f"✓ Variante aggiornata - SKU {sku}: {data_dict}")
                return response
            else:
                product_id = product.get('id')
                response = self._retry_request('put', f"products/{product_id}", data=data_dict)
                logger.debug(f"✓ Prodotto aggiornato - SKU {sku}: {data_dict}")
                return response
        except Exception as e:
            logger.error(f"✗ Errore nell'aggiornamento prodotto SKU {sku}: {e}")
            raise
