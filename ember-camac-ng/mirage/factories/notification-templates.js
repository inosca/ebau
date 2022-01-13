import { faker } from "@faker-js/faker";
import { Factory, association } from "miragejs";

export default Factory.extend({
  purpose: () => faker.lorem.sentence(),
  subject: () => faker.lorem.sentence(),
  body: () => faker.lorem.paragraph(),
  type: "textcomponent",

  service: association(),
});
