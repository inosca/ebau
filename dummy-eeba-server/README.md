## Dummy Service to mock eEBA 

This project includes a local dummy service (`/dummy-eeba`) to simulate the third-party eEBA API for development and testing.

**Usage:**
- The dummy service is only intended for local development & local testing.
- !!! It should never be deployed or exposed in production !!!

### How to Use Locally (only for kt. GR)

1. Start all services:
    ```sh
    docker-compose up -d
    ```
2. The camac django app will use the dummy service if `EEBA_BASE_URL` points to `http://dummy-eeba:9000/dummy-eeba` so in django `.env` file add `EEBA_BASE_URL`:
   ```
    UID=1000
    APPLICATION=kt_gr
    COMPOSE_FILE=compose/kt_gr.yml:compose/kt_gr-dev.yml
    ...
    EEBA_BASE_URL=http://dummy-eeba:9000/dummy-eeba
   ```

### Production Safety

- The dummy service is **not** started in production Docker/Kubernetes deployments.
- The real `EEBA_BASE_URL` (either test or prod) must be used in all non-local environments.

### Troubleshooting

If you see errors related to eEBA integration, check that:
- The dummy-eeba service is running (for local).
- The `EEBA_BASE_URL` env var is set correctly.

Note that the DUMMY_RESOURCES dictionary exists only in memory so a restart of the dummy-eeba service can result in not found responses
