# Theming

There are 3 environments which can be used to theme `ember-camac-ng`:

- `be` for Kt. Bern
- `sz` for Kt. Schwyz
- `ur` for Kt. Uri

If you need to create a style that should only be applied for one
environment, create a file for each environment:
`_your-style-{environment}.scss` and then import it without the environment
postfix: `@import "your-style";`. The build process will automatically rename
the environment specific file to the imported name and remove all unused
files.

The environment will be taken from the `.env` file in the root folder
(fallback is BE). In the container it's passed by docker-compose.
