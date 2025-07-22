# WSGI configuration

It is possible to run the Django application with or without
integrated DAV support. While we primarily use the integrated approach
with the uWSGI application server, it is not exclusive to it.

> Use `wsgi.py` in this case.

Separating the DAV application from the main Django application allows
for independent configuration and scaling. This approach is
particularly useful in cloud-native and high-availability
environments, such as Kubernetes. We have tested this setup with the
Gunicorn application server, which is reflected in the config file
names.

> Use `wsgi_gunicorn.py` and `wsgi_dav.py`.

Running the DAV application separately also makes it possible to use
an asynchronous, non-blocking application server like [Tornado](https://www.tornadoweb.org)
for the django app. While Tornado is not a WSGI-compliant server by
default, it can wrap WSGI applications. In this case, you do not need
to pass any uwsgi related configuration files, as Tornado provides its
own setup.

⚠ Note: Running the camac django application with integrated DAV is not
possible with this approach.
