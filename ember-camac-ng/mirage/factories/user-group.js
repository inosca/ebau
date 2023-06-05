import { faker } from "@faker-js/faker";
import { Factory, association } from "miragejs";

export default Factory.extend({
  createdAt: () => faker.date.past(),

  user: association(),
  group: association(),
  createdBy: association(),
});
