import { faker } from "@faker-js/faker";
import { Factory } from "miragejs";

export default Factory.extend({
  afterCreate(communicationsEntity, server) {
    communicationsEntity.update({
      service: faker.helpers.arrayElement(server.schema.services.all().models),
    });
  },
});
