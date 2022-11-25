import { faker } from "@faker-js/faker";
import { Factory } from "miragejs";

export default Factory.extend({
  body: () =>
    faker.lorem.paragraph({ sentenceCount: faker.datatype.number({ max: 6 }) }),
  created: () => faker.date.recent(),
  isRead: false,
  afterCreate(communicationsMessage, server) {
    server.createList(
      "communications-attachment",
      faker.datatype.number({ max: 5 }),
      { communicationsMessage }
    );
  },
});
