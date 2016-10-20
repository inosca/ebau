import sys

with open("tools/deploy/htaccess_tmpl", "r") as tmpl_file:
    tmpl = tmpl_file.read()


if len(sys.argv) > 1:

    ENV = sys.argv[1]
    if ENV == 'dev':
        env = 'development'

    if ENV == 'ci':
        env = 'ci'

    elif ENV == 'prod':
        env = 'production'

    elif ENV == 'stage':
        env = 'staging'

        with open("tools/deploy/test-server-htaccess") as test_htaccess:
            tmpl += "\n\n"
            tmpl += test_htaccess.read()
    elif ENV == 'test':
        env = 'testing'

else:
    env = 'development'

tmpl = tmpl.replace('{{ENV}}', env)

with open("camac/public/.htaccess", "w") as htaccess:
    htaccess.write(tmpl)
