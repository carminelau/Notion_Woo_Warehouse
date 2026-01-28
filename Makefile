# Makefile per gestire il progetto Stock Management

.PHONY: help build up down logs stop start clean test

help:
	@echo "Stock Management Docker - Comandi Disponibili"
	@echo "=============================================="
	@echo "make build       - Costruisce l'immagine Docker"
	@echo "make up          - Avvia i container"
	@echo "make down        - Ferma i container"
	@echo "make logs        - Visualizza i log in tempo reale"
	@echo "make stop        - Ferma i container (senza rimuoverli)"
	@echo "make start       - Avvia i container arrestati"
	@echo "make clean       - Rimuove container, immagini e volumi"
	@echo "make test        - Testa la connessione ai servizi"
	@echo "make config      - Copia il file .env.example in .env"

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f stock-sync

stop:
	docker-compose stop

start:
	docker-compose start

clean:
	docker-compose down -v
	docker rmi stock-management 2>/dev/null || true

test:
	@echo "Test connessione ai servizi..."
	@docker-compose exec -T stock-sync python -c "from sync.woocommerce_client import WooCommerceClient; print('✓ WooCommerce Client OK')" || echo "✗ Errore WooCommerce"
	@docker-compose exec -T stock-sync python -c "from sync.notion_client import NotionClient; print('✓ Notion Client OK')" || echo "✗ Errore Notion"

config:
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "✓ File .env creato da .env.example"; \
		echo "⚠️  Modifica .env con le tue credenziali!"; \
	else \
		echo "✓ File .env già esistente"; \
	fi
