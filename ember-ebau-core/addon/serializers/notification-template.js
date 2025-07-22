import JSONAPISerializer from "@ember-data/serializer/json-api";

export default class NotificationTemplateSerializer extends JSONAPISerializer {
  serializeAttribute(snapshot, json, key, attributes) {
    if (snapshot.record.isNew || key !== "slug") {
      super.serializeAttribute(snapshot, json, key, attributes);
    }
  }
}
