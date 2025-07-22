import { faker } from "@faker-js/faker";
import { DateTime } from "luxon";
import { Factory } from "miragejs";

export default Factory.extend({
  name() {
    return {
      de: faker.lorem.words(3),
      fr: "",
      it: "",
    };
  },
  leadTime: () => faker.number.int({ min: 1, max: 30 }),
  createdAt: () => DateTime.fromJSDate(faker.date.past()).toISODate(),
});
