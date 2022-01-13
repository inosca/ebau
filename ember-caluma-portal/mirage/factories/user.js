import { faker } from "@faker-js/faker";
import { Factory } from "miragejs";

export default Factory.extend({
  surname: () => faker.name.firstName(),
  name: () => faker.name.lastName(),
  username: () => faker.datatype.uuid(),
});
