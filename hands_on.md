```text
my-fastapi-app/
├── .env.example
├── .python-version
├── pyproject.toml
├── uv.lock
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── dependencies.py
│   │   └── tasks.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── errors.py
│   │   └── logging.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── task.py
│   └── services/
│       ├── __init__.py
│       └── tasks.py
└── tests/
    ├── __init__.py
    ├── test_health.py
    ├── test_task_schemas.py
    ├── test_task_service.py
    └── test_tasks.py
```

