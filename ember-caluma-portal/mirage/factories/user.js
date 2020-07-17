import { Factory } from "ember-cli-mirage";
import faker from "faker";

export default Factory.extend({
  surname: () => faker.name.firstName(),
  name: () => faker.name.lastName(),
  username: () => faker.random.uuid(),
});
