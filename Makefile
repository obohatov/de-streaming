.PHONY: run test

run:
	uvicorn api.api:app --reload

test:
	pytest
	