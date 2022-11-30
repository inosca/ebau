import { faker } from "@faker-js/faker";
import { Factory } from "miragejs";

export default Factory.extend({
  body: () => faker.lorem.paragraph(),
  created: () => faker.date.recent(),
  isRead: false,
});
