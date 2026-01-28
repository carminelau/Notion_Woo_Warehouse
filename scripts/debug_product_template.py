#!/usr/bin/env python3
"""
Template per ispezionare e debuggare prodotti WooCommerce

NOTA: Questo è uno script di test/development per analizzare la struttura
dei tuoi prodotti WooCommerce e capire gli attributi disponibili.

Uso:
    python debug_product_template.py              # Ispeziona primi 5 prodotti
    python debug_product_template.py --sku=ABC    # Ispeziona prodotto con SKU specifico
    python debug_product_template.py --id=123     # Ispeziona prodotto con ID specifico
    python debug_product_template.py --limit=10   # Ispeziona primissimi 10 prodotti
"""

import os
import json
import argparse
from dotenv import load_dotenv
from sync.woocommerce_client import WooCommerceClient

# Carica variabili di ambiente
load_dotenv()

def print_product_info(product, woo_client=None):
    """Stampa informazioni dettagliate su un prodotto"""
    
    product_id = product.get('id')
    product_name = product.get('name', 'N/A')
    product_type = product.get('type', 'simple')
    
    print(f"\n{'='*80}")
    print(f"📦 PRODOTTO DETAILS")
    print(f"{'='*80}")
    print(f"ID: {product_id}")
    print(f"Nome: {product_name}")
    print(f"Tipo: {product_type}")
    print(f"SKU: {product.get('sku', 'VUOTO') or 'VUOTO'}")
    print(f"Prezzo: €{product.get('price', 'N/A')}")
    print(f"Stock: {product.get('stock_quantity', 'N/A')}")
    print(f"Status: {product.get('status', 'N/A')}")
    
    # ATTRIBUTI
    print(f"\n{'─'*80}")
    print("📋 ATTRIBUTI:")
    print(f"{'─'*80}")
    if product.get('attributes'):
        for attr in product.get('attributes', []):
            print(f"  • {attr.get('name', 'N/A')}: {attr.get('option', 'N/A')}")
    else:
        print("  ⊘ Nessun attributo")
    
    # METADATI
    print(f"\n{'─'*80}")
    print("🔧 METADATI:")
    print(f"{'─'*80}")
    if product.get('meta_data'):
        for meta in product.get('meta_data', []):
            print(f"  • {meta.get('key', 'N/A')}: {meta.get('value', 'N/A')}")
    else:
        print("  ⊘ Nessun metadato")
    
    # Se è un prodotto variabile, mostra anche le varianti
    if product_type == 'variable' and woo_client:
        print(f"\n{'─'*80}")
        print("🎨 VARIANTI:")
        print(f"{'─'*80}")
        try:
            variants = woo_client._retry_request(
                'get', 
                f"products/{product_id}/variations", 
                params={"per_page": 5}
            )
            variants = variants if isinstance(variants, list) else [variants]
            
            for v_idx, variant in enumerate(variants, 1):
                v_id = variant.get('id')
                v_sku = variant.get('sku', 'VUOTO')
                v_price = variant.get('price', 'N/A')
                v_stock = variant.get('stock_quantity', 'N/A')
                
                print(f"\n  Variante #{v_idx} (ID: {v_id})")
                print(f"  SKU: {v_sku or 'VUOTO'}")
                print(f"  Prezzo: €{v_price}")
                print(f"  Stock: {v_stock}")
                
                if variant.get('attributes'):
                    print(f"  Attributi:")
                    for attr in variant.get('attributes', []):
                        print(f"    - {attr.get('name')}: {attr.get('option')}")
        except Exception as e:
            print(f"  ⚠️  Errore nel recupero varianti: {e}")
    
    # SALVA JSON PER ANALISI
    json_file = f'debug_product_{product_id}.json'
    try:
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(product, f, ensure_ascii=False, indent=2)
        print(f"\n💾 Salvato in: {json_file}")
    except Exception as e:
        print(f"\n⚠️  Errore salvataggio JSON: {e}")

def main():
    # Argomenti della riga di comando
    parser = argparse.ArgumentParser(description='Debug e analisi prodotti WooCommerce')
    parser.add_argument('--sku', help='Cerca prodotto per SKU')
    parser.add_argument('--id', type=int, help='Cerca prodotto per ID')
    parser.add_argument('--limit', type=int, default=5, help='Numero di prodotti da mostrare (default: 5)')
    args = parser.parse_args()
    
    # Inizializza il client WooCommerce
    api_url = os.getenv('WOOCOMMERCE_API_URL')
    consumer_key = os.getenv('WOOCOMMERCE_CONSUMER_KEY')
    consumer_secret = os.getenv('WOOCOMMERCE_CONSUMER_SECRET')
    
    print("="*80)
    print("🔍 Template: Debug Prodotti WooCommerce")
    print("="*80)
    
    try:
        woo = WooCommerceClient(api_url, consumer_key, consumer_secret)
        
        if args.sku:
            # Cerca per SKU
            print(f"\n🔍 Ricerca prodotto con SKU: {args.sku}")
            product = woo.get_product_by_sku(args.sku)
            if product:
                print_product_info(product, woo)
            else:
                print(f"❌ Prodotto con SKU '{args.sku}' non trovato!")
        
        elif args.id:
            # Cerca per ID
            print(f"\n🔍 Ricerca prodotto con ID: {args.id}")
            product = woo._retry_request('get', f'products/{args.id}')
            if product:
                print_product_info(product, woo)
            else:
                print(f"❌ Prodotto con ID {args.id} non trovato!")
        
        else:
            # Mostra i primi N prodotti
            print(f"\n📥 Recupero primi {args.limit} prodotti da WooCommerce...")
            products_response = woo._retry_request('get', 'products', params={"per_page": args.limit})
            
            if not products_response:
                print("❌ Nessun prodotto trovato!")
                return
            
            products = products_response if isinstance(products_response, list) else [products_response]
            
            for idx, product in enumerate(products, 1):
                print(f"\n\n{'#'*80}")
                print(f"PRODOTTO {idx} di {len(products)}")
                print(f"{'#'*80}")
                print_product_info(product, woo)
        
        print(f"\n\n{'='*80}")
        print("✅ Debug completato!")
        print("💡 Controlla i file .json generati per una visione completa dei dati")
        print(f"{'='*80}\n")
        
    except Exception as e:
        print(f"❌ Errore critico: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
