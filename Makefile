all: down build up install-ollama-gpt-oss 

down:
	@docker compose down --remove-orphans

build:
	@docker compose build

up:
	@docker compose up -d --remove-orphans

logs:
	@docker compose logs -f ${SERVICE}

sh:
	@docker compose exec ${SERVICE} sh

ps:
	@docker compose ps

stats:
	@docker compose stats

install-ollama-gpt-oss:
	@docker compose exec ollama ollama pull gpt-oss:20b

popullate-data-source:
	@python ./populate_sources.py
