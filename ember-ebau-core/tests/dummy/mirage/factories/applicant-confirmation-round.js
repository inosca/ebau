import { faker } from "@faker-js/faker";
import { Factory, association } from "miragejs";

export default Factory.extend({
  id: () => faker.string.uuid({ version: 7 }),
  step: () => faker.helpers.arrayElement(["submit", "additional-demand"]),
  status: () =>
    faker.helpers.arrayElement([
      "running",
      "completed",
      "canaceled",
      "invalidated",
    ]),
  createdAt: () => faker.date.past(),
  closedAt() {
    const from = this.createdAt.getTime();
    const to = Date.now();

    return this.status === "pending" ? null : faker.date.between({ from, to });
  },

  document: association(),
  instance: association(),

  afterCreate(round, server) {
    server.createList(
      "applicant-confirmation",
      faker.number.int({ min: 1, max: 5 }),
      { round },
    );
  },
});
