import { faker } from "@faker-js/faker";
import { Factory } from "miragejs";

export default Factory.extend({
  surname: () => faker.person.firstName(),
  name: () => faker.person.lastName(),
  username: () => faker.string.uuid(),
});
