import JSONSerializer from "@ember-data/serializer/json";

export default class TemplateSerializer extends JSONSerializer {
  primaryKey = "slug";

  // If we don't do this, Ember will interpret the `meta` property in the single
  // response as meta object and omit it from the attributes.
  extractMeta() {}

  // Disable root key serialization since we want to send plain form data
  serializeIntoHash = null;

  serialize(snapshot) {
    const { description, meta, engine, template, slug, availablePlaceholders } =
      snapshot.attributes();

    const formData = new FormData();

    formData.append("slug", slug);
    formData.append("description", description);
    formData.append("meta", JSON.stringify(meta));
    formData.append("engine", engine);

    if (template instanceof File) {
      formData.append("template", template);
      availablePlaceholders.forEach((placeholder) =>
        formData.append("available_placeholders", placeholder)
      );
    }

    return formData;
  }
}
