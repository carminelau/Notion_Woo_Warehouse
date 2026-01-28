#!/usr/bin/env python3
"""
Template per aggiungere SKU automatici ai prodotti WooCommerce

NOTA: Questo è uno script di test/development. Per un uso specifico:
1. Copia questo file con un nome diverso (es: add_custom_skus.py)
2. Modifica il prefisso SKU in generate_sku() secondo le tue necessità
3. Adatta la logica alle tue esigenze

Uso:
    python add_sku_template.py                    # Non sovrascrive SKU esistenti
    python add_sku_template.py --overwrite       # Sovrascrive anche SKU esistenti
"""

import os
import argparse
from dotenv import load_dotenv
from sync.woocommerce_client import WooCommerceClient

# Carica variabili di ambiente
load_dotenv()

def generate_sku(product_id, variant_id=None, prefix="PROD"):
    """
    Genera uno SKU con prefisso personalizzabile
    
    MODIFICA QUESTA FUNZIONE per adattarla alle tue esigenze!
    
    Args:
        product_id: ID del prodotto
        variant_id: ID della variante (opzionale)
        prefix: Prefisso SKU (default: "PROD")
        
    Returns:
        SKU generato con il prefisso
    """
    # TODO: Personalizza il formato SKU qui
    if variant_id:
        return f"{prefix}-{product_id}-V{variant_id}"
    else:
        return f"{prefix}-{product_id}"

def main():
    # Argomenti della riga di comando
    parser = argparse.ArgumentParser(description='Aggiungi SKU automatici ai prodotti WooCommerce')
    parser.add_argument('--overwrite', action='store_true', help='Sovrascrive SKU esistenti')
    parser.add_argument('--prefix', default='PROD', help='Prefisso SKU (default: PROD)')
    parser.add_argument('--limit', type=int, default=None, help='Numero massimo prodotti da elaborare')
    args = parser.parse_args()
    
    # Inizializza il client WooCommerce
    api_url = os.getenv('WOOCOMMERCE_API_URL')
    consumer_key = os.getenv('WOOCOMMERCE_CONSUMER_KEY')
    consumer_secret = os.getenv('WOOCOMMERCE_CONSUMER_SECRET')
    
    print("="*80)
    print("🔧 Template: Aggiunta SKU Automatici a Prodotti WooCommerce")
    print(f"⚙️  Prefisso SKU: {args.prefix}")
    if args.overwrite:
        print("⚠️  MODALITÀ SOVRASCRITTURA ATTIVA")
    if args.limit:
        print(f"📊 Limite prodotti: {args.limit}")
    print("="*80)
    
    try:
        woo = WooCommerceClient(api_url, consumer_key, consumer_secret)
        
        # Recupera tutti i prodotti
        print("\n📥 Recupero prodotti da WooCommerce...")
        per_page = min(args.limit, 100) if args.limit else 100
        products_response = woo._retry_request('get', 'products', params={"per_page": per_page})
        
        if not products_response:
            print("❌ Nessun prodotto trovato!")
            return
        
        products = products_response if isinstance(products_response, list) else [products_response]
        
        # Limita se necessario
        if args.limit:
            products = products[:args.limit]
        
        total_updated = 0
        total_skipped = 0
        total_errors = 0
        
        for idx, product in enumerate(products, 1):
            product_id = product.get('id')
            product_name = product.get('name', 'N/A')
            product_type = product.get('type', 'simple')
            existing_sku = product.get('sku', '')
            
            print(f"\n[{idx}/{len(products)}] 📦 {product_name} (ID: {product_id})")
            
            # Se il prodotto non ha SKU, aggiungilo (o se --overwrite è attivo)
            if not existing_sku or args.overwrite:
                sku = generate_sku(product_id, prefix=args.prefix)
                
                try:
                    # TODO: Personalizza il metodo di update secondo il tuo client
                    woo.update_product_data(existing_sku or sku, {"sku": sku})
                    print(f"  ✅ SKU: {sku}")
                    total_updated += 1
                except Exception as e:
                    print(f"  ❌ Errore: {e}")
                    total_errors += 1
            else:
                print(f"  ⊘ Ha già SKU: {existing_sku}")
                total_skipped += 1
            
            # Se è un prodotto variabile, gestisci le varianti
            if product_type == 'variable':
                try:
                    variants = woo._retry_request(
                        'get',
                        f"products/{product_id}/variations",
                        params={"per_page": 100}
                    )
                    variants = variants if isinstance(variants, list) else [variants]
                    
                    for variant in variants:
                        variant_id = variant.get('id')
                        variant_sku = variant.get('sku', '')
                        
                        if not variant_sku or args.overwrite:
                            sku = generate_sku(product_id, variant_id, prefix=args.prefix)
                            
                            try:
                                woo.update_product_data(variant_sku or sku, {"sku": sku})
                                total_updated += 1
                            except Exception as e:
                                print(f"    ⚠️  Variante {variant_id}: {e}")
                                total_errors += 1
                        else:
                            total_skipped += 1
                            
                except Exception as e:
                    print(f"  ⚠️  Errore varianti: {e}")
        
        print(f"\n{'='*80}")
        print(f"📊 RIEPILOGO")
        print(f"{'='*80}")
        print(f"✅ SKU aggiunti/aggiornati: {total_updated}")
        print(f"⊘ SKU già presenti: {total_skipped}")
        print(f"❌ Errori: {total_errors}")
        print(f"{'='*80}\n")
        
    except Exception as e:
        print(f"❌ Errore critico: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
