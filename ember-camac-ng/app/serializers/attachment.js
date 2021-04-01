import JSONAPISerializer from "@ember-data/serializer/json-api";

export default class AttachmentSerializer extends JSONAPISerializer {
  attrs = {
    path: {
      serialize: false,
    },
  };
}
