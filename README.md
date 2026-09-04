## FASTApi In and outs

This repo is used for learning fastapi, this would later pivot into a repo with a specific use case.

#### Features

- Task CRUD endpoints
- Request validation via Pydantic schemas
- Centralized error handling and logging
- Automated tests
---
#### Project structure

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

#### Prequisites 
- Python 3.14.4
- uv

#### Steps to initiate the application

- `git clone <get the link from the github repo>`
- `cd fast_api_use_case/my-fastapi-app`
- `uv sync`

- `uv run fastapi dev app/main.py`

###### run the development server:

`uv run fastapi dev app/main.py`
- expected output will include a local URL similar to :
                                 
    - Swagger/OpenAPI UI: `http://127.0.0.1:8000/docs`
    - ReDoc documentation: `http://127.0.0.1:8000/redoc`
    - Raw OpenAPI specification: `http://127.0.0.1:8000/openapi.json`


#### Note:
Explanations of each and every code will be present in the hands_on.md 

---
This repository grows one practical FastAPI decision at a time: build it, break it, test it and understand why it works.
---

