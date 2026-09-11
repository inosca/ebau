import { faker } from "@faker-js/faker";
import { DateTime } from "luxon";
import { Factory } from "miragejs";

export default Factory.extend({
  invoiceText: () => faker.lorem.word(),
  dateAdded: () => DateTime.fromJSDate(faker.date.past()).toISODate(),
});
