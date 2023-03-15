# marketplace_api
Simple online marketplace based on FastAPI framework

## How to run a project

### Installing
```bash
git clone https://github.com/ani-zia/marketplace_api.git
```

```bash
cd marketplace_api
```

### 1. Run locally on docker container

1.1. Run Docker

1.2. Run project containers:
```bash
docker-compose -f docker-compose-dev.yaml up -d --build
```

1.3. Check documantation in browser
http://0.0.0.0:8000/docs or http://localhost:8000/docs

### 2. Run locally in terminal

2.1. Install poetry and run shell: https://python-poetry.org/docs/#installation

2.2. Create .env file from env.example and fill it with credentials

2.3. Run Docker

2.4. Start a postgres container
```bash
docker-compose -f postgres-local.yaml up -d --build
```

2.5. Apply migrations:
```bash
alembic upgrade head
```

2.6. Run app
```bash
poetry run task start
```

2.7. Check documantation in browser
http://127.0.0.1:8000/docs
