import JSONAPISerializer from "@ember-data/serializer/json-api";
import { DateTime } from "luxon";

export default class InstanceDeadlineSerializer extends JSONAPISerializer {
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
