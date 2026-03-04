import JSONAPISerializer from "@ember-data/serializer/json-api";
import { DateTime } from "luxon";

export default class SuspensionSerializer extends JSONAPISerializer {
  attrs = {
    // The `reason` field is auto-set by the backend.
    reason: { serialize: false },
    // The `reasonFormatted` field is a backend calculated field.
    reasonFormatted: { serialize: false },
    // The `authorFormatted` field is a backend calculated field.
    authorFormatted: { serialize: false },
    // The `user` field is auto-set by the backend.
    user: { serialize: false },
    // The `group` field is auto-set by the backend.
    group: { serialize: false },
  };

  serializeAttribute(snapshot, json, key, attributes) {
    if (!json.attributes) {
      json.attributes = {};
    }

    const value = snapshot.attr(key);
    if (attributes.type === "date" && typeof value === "object") {
      return (json.attributes[key] = DateTime.fromJSDate(value).toISODate());
    }

    super.serializeAttribute(snapshot, json, key, attributes);
  }
}
