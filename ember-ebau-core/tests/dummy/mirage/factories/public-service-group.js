import { faker } from "@faker-js/faker";
import { Factory } from "miragejs";

export default Factory.extend({
  slug: () => faker.lorem.slug(),
  name: () => faker.lorem.word(),
});
