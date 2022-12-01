import { faker } from "@faker-js/faker";
import { Factory, trait } from "miragejs";

const randomInt = (max = 5) => faker.datatype.number({ max });

export default Factory.extend({
  subject: () => faker.lorem.sentence(),
  created: () => faker.date.recent(),
  hasUnread: () => faker.datatype.boolean(),
  afterCreate(communicationsTopic, server) {
    const initiatedBy = server.schema.users.first() ?? server.create("user");
    const involvedEntities = server.schema.communicationsEntities.all();
    communicationsTopic.update({
      initiatedBy,
      involvedEntities: involvedEntities.length
        ? involvedEntities
        : server.createList("communications-entity", 5),
    });
  },
  withMessages: trait({
    afterCreate(communicationsTopic, server) {
      server.createList("communications-message", randomInt(), {
        communicationsTopic,
        createdBy: server.schema.communicationsEntities.find(randomInt()),
        readBy: server.schema.communicationsEntities.find(
          Array.from(randomInt()).map(() => randomInt())
        ),
        isRead: faker.datatype.boolean(),
      });
    },
  }),
});
