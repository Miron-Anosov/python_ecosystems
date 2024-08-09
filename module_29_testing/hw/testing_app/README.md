TEST RUN:
```bash 
cd ./. && coverage run -m pytest -v -s && coverage report --show-missing
```
OR:
```bash
cd ./.
poetry run pytest --cov=app --cov-report=term-missing
```