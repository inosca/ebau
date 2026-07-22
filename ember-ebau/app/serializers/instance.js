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
    if (relationship.meta.options.readOnly) return;

    // This allows filtering exactly which relationships get serialized to the backend.
    // It was added specifically for the keyword use-case to prevent unnecessary data from being sent.
    // If `patchedRelationships` is undefined, the default behavior is to just save all of them.
    const patchedRelationships = snapshot.adapterOptions?.patchedRelationships;
    if (
      patchedRelationships === undefined ||
      patchedRelationships.includes(relationship.key)
    ) {
      super.serializeHasMany(snapshot, json, relationship);
    }
  }
}
