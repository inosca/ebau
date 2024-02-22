import os

import environ

env = environ.Env()

# resolves to folder django or /app in container
ROOT_DIR = environ.Path(__file__) - 3

ENV_FILE = env.str("DJANGO_ENV_FILE", default=ROOT_DIR(".env"))

# overwrite ENV with contents of .env, except while running pytest
if env.str("APPLICATION_ENV", default="production") != "ci" and os.path.exists(
    ENV_FILE
):  # pragma: no cover
    environ.Env.read_env(ENV_FILE, True)
