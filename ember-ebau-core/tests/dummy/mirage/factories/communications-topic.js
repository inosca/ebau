import { faker } from "@faker-js/faker";
import { Factory } from "miragejs";

const randomInt = (max = 5) => faker.datatype.number({ max });

export default Factory.extend({
  subject: () => faker.lorem.sentence(),
  created: () => faker.date.recent(),
  hasUnread: () => faker.datatype.boolean(),
  afterCreate(communicationsTopic, server) {
    communicationsTopic.update({
      initiatedBy: server.schema.users.first(),
      involvedEntities: server.schema.communicationsEntities.all(),
    });
    server.createList("communications-message", randomInt(), {
      communicationsTopic,
      createdBy: server.schema.communicationsEntities.find(randomInt()),
      readBy: server.schema.communicationsEntities.find(
        Array.from(randomInt()).map(() => randomInt())
      ),
      isRead: faker.datatype.boolean(),
    });
  },
});
