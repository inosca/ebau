# Migrate from postgres 12 to 15 by dump/restore

1. Run the following command to dump the current database:
   `docker exec -it db pg_dumpall -U camac > ~/camac_backup.sql`
2. Shut down your postgres instance/container. `docker compose stop db`
3. Make a backup of your existing volume data directory, this is mostly in `/var/lib/docker/volumes/camacpgdata/_data`
   So: `tar czf ~/camacpgdata-backup-$(date +%Y%m%d).tar.gz -C /var/lib/docker/volumes/camacpgdata/_data .`
4. Remove/recreate the volume
   `docker rm -f db`
   `docker volume rm camacpgdata && docker volume create camacpgdata`
5. Start the new postgres container with the new volume `docker compose up -d`
6. Restore the dump into the new database:
   `cat ~/camac_backup.sql | docker exec -i <new-db-container> psql -U camac`
7. Restart/update the db and django containers `docker compose up -d django db`
8. Check your logs `docker logs -f db` and `docker logs -f django` for any errors
