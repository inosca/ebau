import { faker } from "@faker-js/faker";
import { DateTime } from "luxon";
import { association, Factory } from "miragejs";

export default Factory.extend({
  instance: association(),
  service: association(),
  deadlineType: association(),

  startDate: () => DateTime.fromJSDate(faker.date.past()).toISODate(),
  totalDaysOfSuspension: () => faker.number.int({ min: 1, max: 30 }),
  processDeadlineDays: () => faker.number.int({ min: 1, max: 30 }),
  processDeadlineDate: () =>
    DateTime.fromJSDate(faker.date.future()).toISODate(),
  createdAt: () => DateTime.fromJSDate(faker.date.past()).toISODate(),
});
