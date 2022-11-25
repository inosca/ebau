import { faker } from "@faker-js/faker";
import { Factory } from "miragejs";

const randomInt = (max = 5) => faker.datatype.number({ max });

export default Factory.extend({
  subject: () => faker.lorem.sentence(),
  created: () => faker.date.recent(),
  afterCreate(topic, server) {
    topic.update({
      initiatedBy: server.create("user"),
      involvedEntities: server.schema.communicationsEntities.all(),
    });
    server.createList("communications-message", randomInt(), {
      topic,
      createdBy: server.schema.communicationsEntities.find(randomInt()),
      readBy: server.schema.communicationsEntities.find(
        Array.from(randomInt()).map(() => randomInt())
      ),
      isRead: faker.datatype.boolean(),
    });
  },
});
