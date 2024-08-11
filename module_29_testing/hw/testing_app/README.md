TEST RUN:
```bash 
cd ./. && coverage run -m pytest -v -s && coverage report --show-missing
```
OR:
```bash
cd ./.
poetry run pytest --cov=app --cov-report=term-missing
```
ONLY PARKING:
```bash
 cd ./. && coverage run -m pytest -v -s -m parking && coverage report 
```

WITHOUT PARKING:
```bash
 cd ./. && coverage run -m pytest -v -s -m "not parking" && coverage report

```