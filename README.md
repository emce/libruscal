# LibrusCal

Rest API to sync Librus Time Table with iCloud Calendar

Application will be exposed as Swagger page on configured address (and port).

## Configuration

Edit `config.json`, fill necessary data.

## Docker

Edit `Dockerfile` and `docker-compose.yaml` to align port number with `config.json`.

You can run application by executing command:

`docker compose up -d`

It will build an image and run it.