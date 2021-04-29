import { Factory } from "ember-cli-mirage";
import faker from "faker";

export default Factory.extend({
  name: () => faker.company.companyName(),
  description: () => faker.lorem.sentence(),
  phone: () =>
    [
      "+41",
      faker.datatype.number({ min: 10, max: 99 }),
      faker.datatype.number({ min: 100, max: 999 }),
      faker.datatype.number({ min: 10, max: 99 }),
      faker.datatype.number({ min: 10, max: 99 }),
    ].join(" "),
  zip: () => faker.datatype.number({ min: 1000, max: 9999 }),
  city: () => faker.address.city(),
  address: () => faker.address.streetAddress(),
  email: () => faker.internet.email(),
  website: () => faker.internet.url(),
});
