import { Factory, association } from "ember-cli-mirage";
import faker from "faker";

export default Factory.extend({
  text: () => (Math.random() > 0.5 ? faker.lorem.paragraph() : ""),
  creation_date: () => faker.date.past(),

  user: association(),
  instance: association(),
  service: association()
});
