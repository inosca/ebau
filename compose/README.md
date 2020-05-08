# Docker Compose Setup
We heavily rely on docker-compose to manage our customer-specific dev, ci, stage
and production environments. The goal of the current docker-compose setup is a
fast feedback loop and simplicity.

The GitLab CI build and deploy stages should only build/deploy containers which
a customer actually requires. We DONT want to build a superset of all containers
for every customer release.
