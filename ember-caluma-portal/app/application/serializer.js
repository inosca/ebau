import JSONAPISerializer from "@ember-data/serializer/json-api";

export default class ApplicationSerializer extends JSONAPISerializer {
  serializeAttribute(snapshot, json, key, attributes) {
    // only save dirty attributes
    if (snapshot.record.isNew || snapshot.changedAttributes()[key]) {
      super.serializeAttribute(snapshot, json, key, attributes);
    }
  }

  normalizeSingleResponse(...args) {
    const [, , payload] = args;

    // write the object's meta field to attributes
    if (payload.data.attributes?.meta) {
      payload.data.attributes.meta = payload.data.meta || {};
    }

    return super.normalizeSingleResponse(...args);
  }

  normalizeArrayResponse(...args) {
    const [, , payload] = args;

    payload.data.forEach((record) => {
      if (record.attributes?.meta) {
        record.attributes.meta = record.meta || {};
      }
    });

    return super.normalizeArrayResponse(...args);
  }
}
