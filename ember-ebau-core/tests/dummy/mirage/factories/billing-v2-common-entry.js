import { faker } from "@faker-js/faker";

export default {
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
  remark: () => faker.lorem.sentence(),
};
