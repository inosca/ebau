import { faker } from "@faker-js/faker";
import { Factory } from "miragejs";

export default Factory.extend({
  afterCreate(instance, server) {
    server.createList(
      "communications-topic",
      faker.datatype.number({ max: 10 }),
      {
        instance,
      }
    );
  },
});
