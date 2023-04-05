import { faker } from "@faker-js/faker";
import { Factory, trait } from "miragejs";

const randomInt = (max = 5) => faker.datatype.number({ max });

export default Factory.extend({
  subject: () => faker.lorem.sentence(),
  created: () => faker.date.recent(),
  hasUnread: () => faker.datatype.boolean(),
  dossierNumber: () =>
    `${faker.datatype.datetime().getFullYear()}-${faker.datatype.number(99)}`,
  afterCreate(communicationsTopic, server) {
    const initiatedBy = server.schema.users.first() ?? server.create("user");
    const services = server.schema.services.all();
    communicationsTopic.update({
      initiatedBy,
      involvedEntities: (services.length
        ? services
        : server.createList("service", 5)
      ).models.map((service) => ({ id: service.id, name: service.name })),
    });
  },
  withMessages: trait({
    afterCreate(communicationsTopic, server) {
      server.createList("communications-message", randomInt(), {
        communicationsTopic,
        createdBy: server.schema.services.find(randomInt()),
        readBy: server.schema.services.find(
          Array.from(randomInt()).map(() => randomInt())
        ),
        isRead: faker.datatype.boolean(),
      });
    },
  }),
});
