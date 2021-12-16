import { Factory, association } from "ember-cli-mirage";
import faker from "faker";

const STATUS = ["verified", "failed"];

export default Factory.extend({
  createdAt: () => faker.date.past(),
  status: () => faker.random.arrayElement(STATUS),

  user: association(),
});
