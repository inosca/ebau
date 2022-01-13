import { faker } from "@faker-js/faker";
import { Factory, association } from "miragejs";

const TYPES = ["notification", "status-change"];

export default Factory.extend({
  title: () => faker.lorem.sentence(),
  body: () => (Math.random() > 0.5 ? faker.lorem.paragraph() : ""),
  date: () => faker.date.past(),
  type: () => faker.random.arrayElement(TYPES),

  user: association(),
  instance: association(),
  service: association(),
});
