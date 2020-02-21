# Docker Compose Setup
We heavily rely on docker-compose to manage our customer-specific dev, ci, stage
and production environments. The goal of the current architecture is a fast
feedback loop and simplicity.

The GitLab CI release stages should only build containers which are actually used
by the customer. We DONT want to build a superset of all containers for every
customer release!

We don't gain much from a complex, unified deployment template, therefore each
customer and environment has it's own docker-compose file. This means a lot of
duplication but it's easily understandable.
