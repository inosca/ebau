import { faker } from "@faker-js/faker";
import { Factory } from "miragejs";

export default Factory.extend({
  slug: () => faker.lorem.word(),
  name: () => faker.lorem.word(),
  description: () => faker.lorem.sentence(),
  requiredGrantType: () => faker.helpers.arrayElement(["SERVICE", "USER"]),
});
