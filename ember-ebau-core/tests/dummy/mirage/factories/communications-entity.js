import { faker } from "@faker-js/faker";
import { Factory } from "miragejs";

export default Factory.extend({
  afterCreate(communicationsEntity, server) {
    const services = server.schema.services.all();

    communicationsEntity.update({
      service: faker.helpers.arrayElement(
        services.length ? services.models : server.createList("service", 5)
      ),
    });
  },
});
