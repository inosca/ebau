import JSONAPISerializer from "@ember-data/serializer/json-api";

export default JSONAPISerializer.extend({
  serializeAttribute(snapshot, json, key, attributes) {
    // only save dirty attributes
    if (snapshot.record.isNew || snapshot.changedAttributes()[key]) {
      this._super(snapshot, json, key, attributes);
    }
  },

  normalizeSingleResponse(store, primaryModelClass, payload) {
    // write the object's meta field to attributes
    payload.data.attributes.meta = payload.data.meta || {};

    return this._super(...arguments);
  }
});
