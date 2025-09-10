# Migrate from postgres 12 to 15 by dump/restore

1. Run the following command to dump the current database:
   `docker exec -it compose-db-1 pg_dumpall -U camac > ~/camac_backup.sql`
2. Remove/recreate the volume
   `docker rm -f compose-db-1`
   `docker volume rm camacpgdata && docker volume create camacpgdata`
3. Start the new postgres container with the new volume `git pull`, `docker compose up -d db`
4. Restore the dump into the new database:
   `cat ~/camac_backup.sql | docker exec -i compose-db-1 psql -U camac`
5. Reset the password with the new encryption method:
   `docker exec -it compose-db-1 psql -U camac -c "ALTER USER camac WITH PASSWORD 'yourpassword';"`
   (replace 'yourpassword' with your actual password, stored in `/etc/camac/postgres_password.conf`)
6. Update the db and django containers `docker compose up -d django db`
7. Check your logs `docker logs -f db` and `docker logs -f django` for any errors
