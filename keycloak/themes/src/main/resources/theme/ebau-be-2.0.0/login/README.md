# eBau Kanton Bern Keycloak Theme

This theme is based on the [WebStyleGuide](https://kantonbern.snowflake.ch/styleguides/1/Kanton-Bern/#Gm148)
of the canton of Berne. Most measurements are taken from this style guide and got
translated to re-usable scss stylesheets. The basic layout is configured in the
`template.ftl` and `resources/scss/template-styles.scss`. It's built as a two-
column layout with a main and a context column.

## Configuration

The theme is developed to support third party IdPs in the login form. The basic
login form got removed and won't show up. This theme supports german (de) and
french (fr) by default. If you want to support other languages you have to copy
the messages file and add the new language to the list of supported locales.

### themes.properties

Resource files are listed in here as well as class overrides which will get
interpolated into the page templates. Keycloak delivers a lot of built-in classes
which you have to override/disable once per theme. For custom implementations you
will have to look into the page templates themselves.


### messages/messages_{LANG}.properties
Some messages are used as feature flags to display certain blocks.

* **feedbackbox-message**: Will show a permanent box on the login page in
addition to the keycloak native boxes

## Development

Use `sass` to compile the `css` files from the `scss` sources.

```
sass resources/scss/:resources/css/
```

For developers inside `camac-ng` please use the `build-be` or `watch-be` jobs
defined in the [package.json](../../../../../../package.json).

Adaptation of colors and fonts can be done in the `resources/scss/variables.scss`
file.

