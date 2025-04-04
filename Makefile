.PHONY: po_install po_update db bot clean vanna_app

po_install:
	poetry install

po_update:
	poetry update

vanna_app:
	PYTHONPATH=. poetry run python3 src/vanna_app.py

db:
	PYTHONPATH=. poetry run python3 src/cmd/map_csv_to_sqldb.py

bot:
	PYTHONPATH=. poetry run python3 src/bot.py

clean:
	poetry cache clear --all
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf *.egg-info/
