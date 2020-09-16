# Migrate from postgres 9.5 to 12

1. Shut down your postgres instance/container
2. Make a backup of your existing volume. For staging and prod systems this is mostly in `/var/lib/docker/volumes/camacpgdata/_data`
3. Create a new folder for the converted data, for example `mkdir /var/lib/docker/volumes/camacpgdata/new`
4. Run the following command to convert/migrate the database structure and its data:
`docker run --rm -v /var/lib/docker/volumes/camacpgdata/_data:/var/lib/postgresql/9.5/data -v /var/lib/docker/volumes/camacpgdata/new:/var/lib/postgresql/12/data tianon/postgres-upgrade:9.5-to-12`
5. Delete the content of `/var/lib/docker/volumes/camacpgdata/_data` and copy the content of `/var/lib/docker/volumes/camacpgdata/new` in it
6. Start up (deploy) your new postgres container
7. Check your log of the new container. Sometimes the host permissions seem to be wrong and you get an error with `{ipaddress} not found in pg_hba.conf`. To fix this add the needed ip-addresses or an ip-range to your `pg_hba.conf` in `/var/lib/docker/volumes/camacpgdata/_data`
