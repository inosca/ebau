import JSONAPISerializer from "@ember-data/serializer/json-api";

export default class ApplicationSerializer extends JSONAPISerializer {
  normalizeSingleResponse(...args) {
    const [, , payload] = args;

    // write the object's meta field to attributes
    payload.data.attributes.meta = payload.data.meta || {};

    return super.normalizeSingleResponse(...args);
  }
}
