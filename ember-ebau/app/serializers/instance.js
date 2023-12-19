import JSONAPISerializer from "@ember-data/serializer/json-api";

export default class InstanceSerializer extends JSONAPISerializer {
  serializeAttribute(snapshot, json, key, attributes) {
    // only save dirty attributes
    if (snapshot.record.isNew || snapshot.changedAttributes()[key]) {
      super.serializeAttribute(snapshot, json, key, attributes);
    }
  }

  serializeBelongsTo(snapshot, json, relationship) {
    if (!relationship.meta.options.readOnly) {
      super.serializeBelongsTo(snapshot, json, relationship);
    }
  }

  serializeHasMany(snapshot, json, relationship) {
    if (!relationship.meta.options.readOnly) {
      super.serializeHasMany(snapshot, json, relationship);
    }
  }
}
