import { faker } from "@faker-js/faker";
import { Factory, association } from "miragejs";

export default Factory.extend({
  text: () => faker.lorem.paragraph(),
  creation_date: () => faker.date.past(),

  user: association(),
  instance: association(),
  service: association(),
});
