import { faker } from "@faker-js/faker";
import { DateTime } from "luxon";
import { Factory, association, trait } from "miragejs";

export default Factory.extend({
  text: () => faker.lorem.word(),
  legalBasis: () =>
    `${faker.lorem.word()} §§${faker.number.int({ min: 1, max: 200 })}`,
  costCenter: () => faker.finance.accountNumber(),
  organization: () =>
    faker.helpers.arrayElement(["cantonal", "municipal", null]),
  calculation: () =>
    faker.helpers.arrayElement(["flat", "percentage", "hourly"]),
  taxMode: () =>
    faker.helpers.arrayElement(["exclusive", "inclusive", "exempt"]),
  taxRate: () => faker.helpers.arrayElement(["2.5", "2.6", "7.7", "8.1"]),
  totalCost: () => faker.finance.amount({ min: 1, max: 1000 }),
  percentage: () => faker.finance.amount({ min: 1, max: 100 }),
  hours: () => faker.finance.amount({ min: 1, max: 10 }),
  hourlyRate: () => faker.finance.amount({ min: 150, max: 300 }),
  finalRate: () => faker.finance.amount({ min: 1, max: 1000 }),
  dateAdded: () => DateTime.fromJSDate(faker.date.past()).toISODate(),
  dateCharged: null,

  group: association(),
  user: association(),
  instance: association(),

  charged: trait({
    afterCreate(entry) {
      entry.update({
        dateCharged: DateTime.fromJSDate(
          faker.date.between({
            from: entry.dateAdded,
            to: DateTime.now().toISODate(),
          }),
        ),
      });
    },
  }),
});
