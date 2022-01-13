import { faker } from "@faker-js/faker";
import { Factory, association } from "miragejs";

export default Factory.extend({
  user: association(),
  invitee: association(),
  instance: association(),
  created: () => faker.date.recent(),
});
