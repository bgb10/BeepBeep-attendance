.PHONY: local
local:
	docker-compose down
	docker-compose up message-broker -d
	@sleep 3
	cd command-server/app && uvicorn main:app --host 0.0.0.0 --port 8000 --reload
