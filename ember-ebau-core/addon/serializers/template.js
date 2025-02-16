import { underscore } from "@ember/string";
import JSONSerializer from "@ember-data/serializer/json";

/*
 * If pagination is enabled in the backend, the response format will be changed.
 * The response data will be wrapped in a `results` object.
 * This would need some configurable normalizer functionality to work.
 */
export default class TemplateSerializer extends JSONSerializer {
  primaryKey = "slug";

  // If we don't do this, Ember will interpret the `meta` property in the single
  // response as meta object and omit it from the attributes.
  extractMeta() {}

  // Disable root key serialization since we want to send plain form data
  serializeIntoHash = null;

  keyForAttribute(key) {
    return underscore(key);
  }

  serialize(snapshot) {
    const {
      description,
      meta,
      engine,
      template,
      slug,
      availablePlaceholders,
      group,
    } = snapshot.attributes();

    const formData = new FormData();

    formData.append("slug", slug);
    formData.append("description", description);
    formData.append("group", group);
    formData.append("meta", JSON.stringify(meta));
    formData.append("engine", engine);

    if (template instanceof File) {
      formData.append("template", template);
      formData.append(
        "available_placeholders",
        JSON.stringify(availablePlaceholders),
      );
    }

    return formData;
  }
}
