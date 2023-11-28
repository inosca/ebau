import { faker } from "@faker-js/faker";
import { Factory } from "miragejs";

export default Factory.extend({
  slug: () => faker.lorem.word(),
  name: () => ({ de: faker.lorem.word() }),
  description: () => ({ de: faker.lorem.word() }),
  requiredGrantType: () => faker.helpers.arrayElement(["SERVICE", "USER"]),
});
