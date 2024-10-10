# AAS-Data-API
A FastAPI service focused on access data from an AAS and show through a dashboard

## Endpoints

#### GET /healthcheck
```bash
curl -X "GET" "http://localhost:5000/healthcheck"
```
```json
{"status": "ok"}
```

#### POST /users/

```bash
curl -X "POST" \
  "http://127.0.0.1:5000/users/" \
  -d '{
      "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
      "username": "username",
      "first_name": "string",
      "last_name": "string"
  }'
```
```json
{
  "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "username": "username",
  "first_name": "string",
  "last_name": "string",
  "deleted": false
}
```

#### GET /users/
```bash
curl -X "GET" "http://127.0.0.1:5000/users/?offset=0&limit=1000&order=asc"
# Equivalent to http://127.0.0.1:5000/users/
```
```json
{
  "users": [
    {
      "id": "3fa85f64-5717-4562-b3fc-2c963f66ffa6",
      "username": "username",
      "first_name": "string",
      "last_name": "string",
      "deleted": false
    },
    {
      "id": "3fa85f64-5717-4562-b3fc-2c9f3f66ffa1",
      "first_name": "string",
      "last_name": "string",
      "deleted": true
    }
  ]
}
```

## Dependencies

### Infrastructure

- [Postgres](https://www.postgresql.org/docs/current/index.html) — Database
- [RabbitMQ](https://www.rabbitmq.com/) — The queue used to publish events
- [Docker](https://docs.docker.com/) — For deployment


###  Key python libs

- [FastAPI](https://fastapi.tiangolo.com/) — Async web framework
- [SQLAlchemy 2.0](https://docs.sqlalchemy.org/en/20/) — ORM for working with database
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) — Database schema migration 
### TODO

- [ ] Implement outbox pattern
- [X] Add auto-tests
- [X] Configure CI
