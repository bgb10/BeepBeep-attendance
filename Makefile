.PHONY: local
local:
	docker-compose down
	docker-compose up message-broker -d
	uvicorn command-server.app.main:app --host 0.0.0.0 --port 8000 --reload
