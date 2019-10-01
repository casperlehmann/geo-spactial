install:
	pip install -r requirements.txt

unittest:
	pytest tests/tests.py

coverage:
	pytest --cov-report=term --cov-report=html --cov=api --cov=worker --cov-config=.coveragerc tests/tests.py

dcup:
	docker-compose up --build
