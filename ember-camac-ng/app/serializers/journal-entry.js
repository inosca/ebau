import JSONAPISerializer from "@ember-data/serializer/json-api";

export default class JournalEntrySerializer extends JSONAPISerializer {
  serialize(...args) {
    const json = super.serialize(...args);

    const duration = json.data.attributes.duration;
    json.data.attributes.duration = duration ? `${duration}:00` : duration;

    return json;
  }
}
