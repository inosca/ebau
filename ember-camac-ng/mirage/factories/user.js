import { Factory } from "ember-cli-mirage";
import faker from "faker";

export default Factory.extend({
  name: () => faker.name.firstName(),
  surname: () => faker.name.lastName(),
});
