import { faker } from "@faker-js/faker";
import { DateTime } from "luxon";
import { association, Factory } from "miragejs";

const REASONS = ["manual_suspension", "additional_demand_suspension"];

export default Factory.extend({
  deadline: association("instance-deadline"),
  group: association(),
  user: association(),

  startDate: () => DateTime.fromJSDate(faker.date.past()).toISODate(),
  endDate: () => DateTime.fromJSDate(faker.date.future()).toISODate(),
  reason: () => faker.helpers.arrayElement(REASONS),
  remark: () => faker.lorem.sentence(),
  createdAt: () => DateTime.fromJSDate(faker.date.past()).toISODate(),
});
