# SWAGGER for Camac eCH0211 API 

The swagger API documentation is configured in `settings.APPLICATION` on a per config-basis.

It is currently used only for the `ECH0211` API which is configured in the settings key of the same name.

In order to make sure that only the required functionalities are exposed to clients it is neccessary to define specific views and urls for the configuration in question. These are defined in the `VIEW_PATH` and the `URL_CLASS` bits of the config.

Any subapp's views are by default included in the swagger docu unless excluded with the `swagger_schema=None` property. For convenience entire subapps's views can be excluded by adding their app-name to the `EXCLUDE_DOCS` list.



