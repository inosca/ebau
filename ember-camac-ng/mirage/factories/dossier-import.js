import { faker } from "@faker-js/faker";
import { Factory, association } from "miragejs";

const STATUS = ["verified", "failed"];

export default Factory.extend({
  createdAt: () => faker.date.past(),
  status: () => faker.random.arrayElement(STATUS),

  user: association(),
});
