# Garage setup

## initial setup

The entrypoint.sh of the garage container will bootstrap the setup on first run:

- setup keys (garage doesn't allow a user:secret key like minio, instead we use an access key and a secret)
- create buckets

See `garage/entrypoint.sh`

## Domain-/Path-based access

Garage uses domain based buckets. If you want to use a single domain, use the proxy
to match the bucket name and use it as a subdomain for the proxy request to garage,
and strip the bucket name from the path.

See `proxy/kt_gr.conf` for both examples.

**Note:** direct access to the buckets only works if the bucket has web-access enabled.

## Buckets

3 buckets will be created:

- `ebau-media` -> `http://ebau-media.garage.localhost/` or `http://garage.localhost/ebau-media/`
- `alexandria-media` -> `http://alexandria-media.garage.localhost/` or `http://garage.localhost/alexandria-media/`
- `dms-media` -> `http://dms-media.garage.localhost/` or `http://garage.localhost/dms-media/`

## Local CLI access

    alias garage='docker exec -ti compose-garage-1 garage'
    garage status

## check web UI

Open http://localhost:3909/buckets after starting the compose setup to inspect the buckets.

**Note:** Your docker compose file will need a separate web ui container with the image `khairul169/garage-webui`.

See `compose/kt_gr-dev.yml` as an example.
