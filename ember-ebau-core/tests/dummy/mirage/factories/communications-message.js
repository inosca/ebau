import { faker } from "@faker-js/faker";
import { Factory } from "miragejs";

export default Factory.extend({
  body: () => faker.lorem.paragraph(),
  createdAt: () => faker.date.past(),
  readAt: () => faker.date.recent(),
  readByEntity: () => [],

  afterCreate(message, server) {
    const createdBy =
      server.schema.services.first() ?? server.create("service");
    const createdByUser = server.schema.users.first() ?? server.create("user");
    const services = server.schema.services.all();
    message.update({
      createdByUser,
      createdBy: { id: createdBy.id, name: createdBy.name },
      readByEntity: (services.length
        ? services.models
        : server.createList("service", 5)
      ).map((service) => ({ id: service.id, name: service.name })),
    });
  },
});
