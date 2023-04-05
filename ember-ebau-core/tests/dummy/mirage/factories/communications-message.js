import { faker } from "@faker-js/faker";
import { Factory } from "miragejs";

export default Factory.extend({
  body: () => faker.lorem.paragraph(),
  createdAt: () => faker.date.recent(),
  isRead: false,
});
