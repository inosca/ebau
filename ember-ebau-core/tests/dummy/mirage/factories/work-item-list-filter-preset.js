import { faker } from "@faker-js/faker";
import { Factory } from "miragejs";

export default Factory.extend({
  name: () => faker.lorem.word(),
  category: faker.helpers.arrayElement([
    "STANDARD",
    "SERVICE",
    "SERVICE_GROUP",
  ]),
  queryParams: () => ({}),
});
