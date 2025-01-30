import { faker } from "@faker-js/faker";
import { Factory } from "miragejs";

import commonEntry from "./billing-v2-common-entry";

export default Factory.extend({
  ...commonEntry,
  name: () => faker.lorem.word(),
  hint: () => faker.lorem.sentence(),
});
