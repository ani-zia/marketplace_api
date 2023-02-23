# marketplace_api
Simple online marketplace based on FastAPI framework

## Preparing

Install poetry and run shell: https://python-poetry.org/docs/#installation

## How to run a project

1. Run Docker

2. Start a postgres container
```bash
docker-compose -f postgres-local.yaml up -d --build
```

3. Apply migrations:
```bash
alembic upgrade head
```

4. Run app
```bash
poetry run task start
```

5. Check documantation in browser
http://127.0.0.1:8000/docs
