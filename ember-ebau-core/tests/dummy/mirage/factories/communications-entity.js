import { Factory } from "miragejs";

export default Factory.extend({
  afterCreate(communicationsEntity, server) {
    communicationsEntity.update({
      service: server.create("service"),
    });
  },
});
