# Compose

- `docker-compose.m1.yml`: durable control plane, MySQL, solver worker and asset server.
- `docker-compose.m2.yml`: M1 topology plus Planning Agent, Prometheus and Grafana.

```bash
docker compose --env-file ../../.env -f docker-compose.m2.yml up --build
```

Service endpoints: control plane `8101`, Planning Agent `8200`, Prometheus `9090`, Grafana `3000`, assets `5001`.
