import { Factory, association } from "ember-cli-mirage";
import faker from "faker";

export default Factory.extend({
  purpose: () => faker.lorem.sentence(),
  subject: () => faker.lorem.sentence(),
  body: () => (Math.random() > 0.5 ? faker.lorem.paragraph() : ""),
  type: "textcomponent",

  service: association(),
});
