import { faker } from "@faker-js/faker";
import { Factory } from "miragejs";

export default Factory.extend({
  name: () => faker.company.name(),
  description: () => faker.lorem.sentence(),
  phone: () =>
    [
      "+41",
      faker.number.int({ min: 10, max: 99 }),
      faker.number.int({ min: 100, max: 999 }),
      faker.number.int({ min: 10, max: 99 }),
      faker.number.int({ min: 10, max: 99 }),
    ].join(" "),
  zip: () => faker.number.int({ min: 1000, max: 9999 }),
  city: () => faker.location.city(),
  address: () => faker.location.streetAddress(),
  email: () => faker.internet.email(),
  website: () => faker.internet.url(),
});
