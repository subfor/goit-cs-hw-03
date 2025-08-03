source init.sh
docker-compose --env-file .env.prod up -d

# PostgreSQL Tasks Seeding

## Setup

cp env.example .env

```bash
source ./init.sh
docker-compose up -d
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

#Task1 PostgreSQL

```
python task_1/init_db.py
python task_1/seed.py
```

#Task2 MongoDB (PyMongo)

```
python task_2/main.py
```
