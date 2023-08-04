import { faker } from "@faker-js/faker";
import { Factory, trait } from "miragejs";

const randomInt = (max = 5) => faker.number.int({ max });

export default Factory.extend({
  subject: () => faker.lorem.sentence(),
  created: () => faker.date.recent(),
  hasUnread: () => faker.datatype.boolean(),
  dossierNumber: () =>
    `${faker.date.anytime().getFullYear()}-${faker.number.int()}`,
  afterCreate(communicationsTopic, server) {
    const initiatedBy = server.schema.users.first() ?? server.create("user");
    const initiatedByEntity = server.create("service", {
      users: [initiatedBy],
    });
    const services = server.schema.services.all();
    communicationsTopic.update({
      initiatedBy,
      initiatedByEntity: {
        id: initiatedByEntity.id,
        name: initiatedByEntity.name,
      },
      involvedEntities: (services.length
        ? services.models
        : server.createList("service", 5)
      ).map((service) => ({ id: service.id, name: service.name })),
    });
  },
  withMessages: trait({
    afterCreate(communicationsTopic, server) {
      server.createList("communications-message", randomInt(), {
        topic: communicationsTopic,
      });
    },
  }),
});
