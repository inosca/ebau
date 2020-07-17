import { Factory, association } from "ember-cli-mirage";
import faker from "faker";

export default Factory.extend({
  user: association(),
  invitee: association(),
  instance: association(),
  created: () => faker.date.recent(),
});
