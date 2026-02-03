import { faker } from "@faker-js/faker";
import { Factory } from "miragejs";

export default Factory.extend({
  code: () => faker.string.alphanumeric(10).toLowerCase(),
  label: () => faker.lorem.words(3),
});
