# Migrate from postgres 9.5 to 12

1. Shut down your postgres instance/container. Sounds simple, but turns out to be hard when you're running inside docker. Solution based on https://github.com/tianon/docker-postgres-upgrade/issues/15:

    ```
    docker exec -it compose_db_1 bash
    su - postgres
    cd /usr/lib/postgresql/9.5/bin
    ./pg_ctl stop
    ```

    If you realize this too late (after the old container is gone for good) you can run `docker run --rm -it -v /var/lib/docker/volumes/camacpgdata/_data/:/var/lib/postgresql tianon/postgres-upgrade:9.5-to-12 bash` and first _start_ the DB using pg_ctl and the stop it.

2. Make a backup of your existing volume. For staging and prod systems this is mostly in `/var/lib/docker/volumes/camacpgdata/_data`
3. Create a new folder for the converted data, for example `mkdir /var/lib/docker/volumes/camacpgdata/new`
4. Run the following command to convert/migrate the database structure and its data:
`docker run --rm -v /var/lib/docker/volumes/camacpgdata/_data:/var/lib/postgresql/9.5/data -v /var/lib/docker/volumes/camacpgdata/new:/var/lib/postgresql/12/data tianon/postgres-upgrade:9.5-to-12`
5. Delete the content of `/var/lib/docker/volumes/camacpgdata/_data` and copy the content of `/var/lib/docker/volumes/camacpgdata/new` in it
6. Start up (deploy) your new postgres container
7. Check your log of the new container. Sometimes the host permissions seem to be wrong and you get an error with `{ipaddress} not found in pg_hba.conf`. To fix this add the needed ip-addresses or an ip-range (e.g. `172.21.0.0/16`) to your `pg_hba.conf` in `/var/lib/docker/volumes/camacpgdata/_data`
